from datetime import datetime
from typing import Optional, List
from xml.etree.ElementTree import Element

from core.models.monetary_obligation import MonetaryObligation
from core.models.obligatory_payments_non_from_entrepreneurship import ObligatoryPaymentsNonFromEntrepreneurship


class CreditorNonFromEntrepreneurship:
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

        self.obligatory_payments_non_from_entrepreneurship: List[ObligatoryPaymentsNonFromEntrepreneurship] = []
        self.monetary_obligations: List[MonetaryObligation] = []


    @classmethod
    def from_xml(cls, element: Element, message_id: str):
        """
        Создаёт экземпляр CreditorNonFromEntrepreneurship из XML-элемента.

        Парсит вложенные элементы ObligatoryPayments и MonetaryObligations,
        создавая соответствующие объекты платежей.

        :param element: XML-элемент с данными кредитора.
        :param message_id: Идентификатор сообщения, к которому относится кредитор.
        :return: Экземпляр CreditorNonFromEntrepreneurship.
        """

        creditor = cls(message_id=message_id)

        obligatory_payments_el = element.find("ObligatoryPayments")
        if obligatory_payments_el is not None:
            for pay_el in obligatory_payments_el.findall("ObligatoryPayment"):
                payment = ObligatoryPaymentsNonFromEntrepreneurship.from_xml(pay_el)
                creditor.obligatory_payments_non_from_entrepreneurship.append(payment)

        monetary_obligations_el = element.find("MonetaryObligations")
        if monetary_obligations_el is not None:
            for pay_el in monetary_obligations_el.findall("MonetaryObligation"):
                payment = MonetaryObligation.from_xml(pay_el)
                creditor.monetary_obligations.append(payment)

        return creditor


    def create(self, conn) -> int:
        """
        Сохраняет кредитора и связанные с ним платежи в базе данных.

        Вставляет запись в таблицу creditors_non_from_entrepreneurship,
        а также сохраняет обязательные платежи и денежные обязательства.

        :param conn: Соединение с базой данных SQLite.
        :return: ID созданной записи кредитора.
        """

        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO creditors_non_from_entrepreneurship (
                message_id, created_at, updated_at
            )
            VALUES (?, ?, ?)
            """,
            (self.message_id, self.created_at, self.updated_at)
        )
        self.id = cursor.lastrowid

        # Вставляем платежи
        for payment in self.obligatory_payments_non_from_entrepreneurship:
            payment.creditor_non_id = self.id
            payment.create(conn)

        for payment in self.monetary_obligations:
            payment.creditor_non_id = self.id
            payment.create(conn)

        conn.commit()
        return self.id
