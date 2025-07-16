"""

"""
from datetime import datetime
from typing import Optional, List
from xml.etree.ElementTree import Element
from core.db.connection import get_connection
from core.models.bank import Bank
from core.models.creditors_from_entrepreneurship import CreditorFromEntrepreneurship
from core.models.creditors_non_from_entrepreneurship import CreditorNonFromEntrepreneurship
from core.models.debtor import Debtor
from core.models.extrajudicial_bankruptcy_message_bank import ExtrajudicialBankruptcyMessageBank
from core.models.message_type import MessageType
from core.models.publisher import Publisher


class ExtrajudicialBankruptcyMessage:
    def __init__(
        self,
        id: str,
        number: Optional[str] = None,
        publish_date: Optional[str] = None,
        finish_reason: Optional[str] = None,
        type_id: Optional[int] = None,
        publisher_id: Optional[int] = None,
        debtor_id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        self.id = id
        self.number = number
        self.publish_date = publish_date
        self.finish_reason = finish_reason
        self.type_id = type_id
        self.publisher_id = publisher_id
        self.debtor_id = debtor_id
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()

        self.banks: List[Bank] = []
        self.creditors_from: Optional[CreditorFromEntrepreneurship] = None
        self.creditors_non: Optional[CreditorNonFromEntrepreneurship] = None

    @classmethod
    def from_xml(cls, element: Element):
        """
        Создаёт объект ExtrajudicialBankruptcyMessage из XML-элемента.

        Извлекает основные поля сообщения, а также связанные сущности:
        тип сообщения, издатель, должник, банки и кредиторов.

        :param element: XML-элемент с данными сообщения.
        :return: Экземпляр ExtrajudicialBankruptcyMessage.
        """

        message_id = element.findtext("Id")
        number = element.findtext("Number")
        publish_date = element.findtext("PublishDate")
        finish_reason = element.findtext("FinishReason")

        # Тип сообщения
        type_el = element.find("Type")
        type_id = None
        if type_el is not None:
            message_type = MessageType.from_xml(type_el)
            type_id = message_type.get_or_create(get_connection())

        # Издатель
        publisher_el = element.find("Publisher")
        publisher_id = None
        if publisher_el is not None:
            publisher = Publisher.from_xml(publisher_el)
            publisher_id = publisher.get_or_create(get_connection())

        # Должник
        debtor_el = element.find("Debtor")
        debtor_obj = None
        if debtor_el is not None:
            debtor_obj = Debtor.from_xml(debtor_el)

        message = cls(message_id, number, publish_date, finish_reason, type_id, publisher_id)
        message.debtor = debtor_obj

        # Банки
        banks_el = element.find("Banks")
        if banks_el is not None:
            for bank_el in banks_el.findall("Bank"):
                bank = Bank.from_xml(bank_el)
                message.banks.append(bank)

        # Группы кредиторов
        from_el = element.find("CreditorsFromEntrepreneurship")
        if from_el is not None:
            message.creditors_from = CreditorFromEntrepreneurship.from_xml(from_el, message_id)

        non_from_el = element.find("CreditorsNonFromEntrepreneurship")
        if non_from_el is not None:
            message.creditors_non = CreditorNonFromEntrepreneurship.from_xml(non_from_el, message_id)

        return message

    def create(self, conn):
        """
        Сохраняет сообщение и связанные с ним данные в базу данных.

        Вставляет запись в таблицу extrajudicial_bankruptcy_message, затем
        сохраняет связанные банки, связь с банками и группы кредиторов.

        :param conn: Соединение с базой данных SQLite.
        """

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO extrajudicial_bankruptcy_message (
                id, number, publish_date, finish_reason,
                type_id, publisher_id, debtor_id,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                self.id, self.number, self.publish_date, self.finish_reason,
                self.type_id, self.publisher_id, self.debtor_id,
                self.created_at, self.updated_at
            )
        )

        # Сохраняем банки
        for bank in self.banks:
            bank.message_id = self.id
            bank.get_or_create(conn)

        # Сохраняем связь банков с сообщением
        for bank in self.banks:
            bank_id = bank.get_or_create(conn)
            link = ExtrajudicialBankruptcyMessageBank(message_id=self.id, bank_id=bank_id)
            link.create(conn)

        # Сохраняем группы кредиторов
        if self.creditors_from:
            self.creditors_from.message_id = self.id
            self.creditors_from.create(conn)

        if self.creditors_non:
            self.creditors_non.message_id = self.id
            self.creditors_non.create(conn)

        conn.commit()

    def exists(self, conn):
        """
        Проверяет, существует ли сообщение в базе по его идентификатору.

        :param conn: Соединение с базой данных SQLite.
        :return: True, если запись существует, иначе False.
        """
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM extrajudicial_bankruptcy_message WHERE id = ?", (self.id,)
        )
        return cursor.fetchone() is not None
