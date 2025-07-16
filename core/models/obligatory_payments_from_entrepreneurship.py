"""
Модель обязательных платежей, связанных с предпринимательской деятельностью.
"""
from datetime import datetime
from xml.etree.ElementTree import Element
from typing import Optional

from core.utils.parser import parse_float


class ObligatoryPaymentsFromEntrepreneurship:
    def __init__(
        self,
        creditor_from_id: int,
        name: Optional[str] = None,
        sum: Optional[float] = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.creditor_from_id = creditor_from_id
        self.name = name
        self.sum = sum
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()

    @classmethod
    def from_xml(cls, element: Element):
        """
        Создаёт объект из XML-элемента.

        :param element: XML-элемент <ObligatoryPaymentsFromEntrepreneurship>.
        :return: Экземпляр ObligatoryPaymentsFromEntrepreneurship.
        """
        name = element.findtext("Name")
        sum_val = parse_float(element.findtext("Sum"))
        return cls(
            creditor_from_id=None,
            name=name,
            sum=sum_val
        )

    def create(self, conn) -> int:
        """
        Сохраняет объект в базу данных и возвращает ID записи.

        :param conn: SQLite-соединение.
        :return: ID созданной записи.
        """

        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO obligatory_payments_from_entrepreneurship (
                creditor_from_id, name, sum, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                self.creditor_from_id, self.name, self.sum, self.created_at, self.updated_at,
            )
        )
        self.id = cursor.lastrowid
        conn.commit()
        return self.id
