"""

"""
from datetime import datetime
from xml.etree.ElementTree import Element
from typing import Optional
from core.utils.parser import parse_float


class MonetaryObligation:
    def __init__(
        self,
        creditor_name: str,
        content: Optional[str] = None,
        basis: Optional[str] = None,
        total_sum: Optional[float] = None,
        debt_sum: Optional[float] = None,
        penalty_sum: Optional[float] = None,
        creditor_non_id: Optional[int] = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.creditor_non_id = creditor_non_id
        self.creditor_name = creditor_name
        self.content = content
        self.basis = basis
        self.total_sum = total_sum
        self.debt_sum = debt_sum
        self.penalty_sum = penalty_sum
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()

    @classmethod
    def from_xml(cls, element: Element):
        """
        Создаёт экземпляр MonetaryObligation из XML-элемента.

        :param element: XML-элемент <MonetaryObligation>.
        :return: Новый экземпляр MonetaryObligation.
        """

        creditor_name = element.findtext("CreditorName")
        content = element.findtext("Content")
        basis = element.findtext("Basis")
        total_sum = parse_float(element.findtext("TotalSum"))
        debt_sum = parse_float(element.findtext("DebtSum"))
        penalty_sum = parse_float(element.findtext("PenaltySum"))


        return cls(
            creditor_non_id=None,
            creditor_name=creditor_name,
            content=content,
            basis=basis,
            total_sum=total_sum,
            debt_sum=debt_sum,
            penalty_sum=penalty_sum
        )

    def create(self, conn) -> int:
        """
        Сохраняет объект в базу данных и возвращает идентификатор записи.

        :param conn: SQLite-соединение.
        :return: ID созданной записи в таблице monetary_obligations.
        """

        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO monetary_obligations (
                creditor_non_id, creditor_name, content, basis, total_sum, 
                debt_sum, penalty_sum, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                self.creditor_non_id, self.creditor_name, self.content, self.basis, self.total_sum,
                self.debt_sum, self.penalty_sum, self.created_at, self.updated_at
            )
        )
        self.id = cursor.lastrowid

        conn.commit()
        return self.id



