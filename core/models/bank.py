"""

"""
from datetime import datetime
from typing import Optional, List
from xml.etree.ElementTree import Element


class Bank:
    def __init__(
        self,
        name: str,
        bik: Optional[str] = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        self.id = id
        self.name = name
        self.bik = bik
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()

    @classmethod
    def from_xml(cls, element: Element):
        """
        Создаёт экземпляр Bank из XML-элемента.

        :param element: XML-элемент с данными банка.
        :return: Экземпляр Bank.
        """

        name = element.findtext("Name")
        bik = element.findtext("Bik")

        bank = cls(name, bik)

        return bank

    def get_or_create(self, conn) -> int:
        """
        Пытается найти банк в базе по БИК или имени, если не найден — создаёт новую запись.

        :param conn: Соединение с базой данных.
        :return: ID существующей или созданной записи банка.
        """

        cursor = conn.cursor()

        # Проверка по БИК
        if self.bik:
            cursor.execute("SELECT id FROM bank WHERE bik =?", (self.bik,))
        elif self.name:
            cursor.execute("SELECT id FROM bank WHERE name = ?", (self.name,))
        else:
            raise ValueError("Не указан BIK или NAME для поиска/создания банка")

        existing = cursor.fetchone()
        if existing:
            self.id = existing[0]
            return self.id

        cursor.execute(
            """
            INSERT INTO bank (name, bik, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            """,
            (self.name, self.bik, self.created_at, self.updated_at)
        )
        self.id = cursor.lastrowid

        conn.commit()
        return self.id