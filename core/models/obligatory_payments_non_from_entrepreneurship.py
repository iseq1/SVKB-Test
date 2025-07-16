"""
Модель обязательных платежей, не связанных с предпринимательской деятельностью.
"""
from datetime import datetime
from xml.etree.ElementTree import Element
from typing import Optional
from core.utils.parser import parse_float


class ObligatoryPaymentsNonFromEntrepreneurship:
    def __init__(
        self,
        creditor_non_id: int,
        name: Optional[str] = None,
        sum: Optional[float] = None,
        penalty_sum: Optional[float] = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.creditor_non_id = creditor_non_id
        self.name = name
        self.sum = sum
        self.penalty_sum = penalty_sum
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()

    @classmethod
    def from_xml(cls, element: Element):
        """
        Создаёт объект из XML-элемента.

        :param element: XML-элемент <ObligatoryPaymentsNonFromEntrepreneurship>.
        :return: Экземпляр ObligatoryPaymentsNonFromEntrepreneurship.
        """
        name = element.findtext("Name")
        sum = parse_float(element.findtext("Sum"))
        penalty_sum = parse_float(element.findtext("PenaltySum"))
        return cls(
            creditor_non_id=None,
            name=name,
            sum=sum,
            penalty_sum=penalty_sum
        )

    def create(self, conn) -> int:
        """
        Создаёт новую запись в таблице obligatory_payments_non_from_entrepreneurship.

        :param conn: SQLite-соединение.
        :return: ID созданной записи.
        """
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO obligatory_payments_non_from_entrepreneurship (
                creditor_non_id, name, sum, penalty_sum,
                created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                self.creditor_non_id, self.name, self.sum, self.penalty_sum,
                self.created_at, self.updated_at
            )
        )
        self.id = cursor.lastrowid
        conn.commit()
        return self.id

