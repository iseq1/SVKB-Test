from datetime import datetime
from typing import Optional, List
from xml.etree.ElementTree import Element

from core.models.obligatory_payments_from_entrepreneurship import ObligatoryPaymentsFromEntrepreneurship


class CreditorFromEntrepreneurship:
    def __init__(
        self,
        message_id: str,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.message_id = message_id
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()

        self.obligatory_payments_from_entrepreneurship: List[ObligatoryPaymentsFromEntrepreneurship] = []

    @classmethod
    def from_xml(cls, element: Element, message_id: str):
        """
        Создаёт экземпляр CreditorFromEntrepreneurship из XML-элемента.

        Парсит вложенный элемент ObligatoryPayments и создаёт объекты обязательных платежей.

        :param element: XML-элемент с данными кредитора.
        :param message_id: Идентификатор сообщения, к которому относится кредитор.
        :return: Экземпляр CreditorFromEntrepreneurship.
        """

        creditor = cls(message_id=message_id)

        obligatory_payments_el = element.find("ObligatoryPayments")
        if obligatory_payments_el is not None:
            for pay_el in obligatory_payments_el.findall("ObligatoryPayment"):
                payment = ObligatoryPaymentsFromEntrepreneurship.from_xml(pay_el)
                creditor.obligatory_payments_from_entrepreneurship.append(payment)

        return creditor

    def create(self, conn) -> int:
        """
        Сохраняет кредитора и связанные с ним обязательные платежи в базе данных.

        Вставляет запись в таблицу creditors_from_entrepreneurship,
        а также сохраняет обязательные платежи из entrepreneurship.

        :param conn: Соединение с базой данных SQLite.
        :return: ID созданной записи кредитора.
        """

        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO creditors_from_entrepreneurship (
                message_id, created_at, updated_at
            )
            VALUES (?, ?, ?)
            """,
            (self.message_id, self.created_at, self.updated_at)
        )
        self.id = cursor.lastrowid

        # Вставляем платежи
        for payment in self.obligatory_payments_from_entrepreneurship:
            payment.creditor_from_id = self.id
            payment.create(conn)

        conn.commit()
        return self.id
