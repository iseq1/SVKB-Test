"""
Модель Publisher (издатель) для хранения и обработки данных из XML.
"""
from datetime import datetime
from typing import Optional, List
from xml.etree.ElementTree import Element

class Publisher:
    def __init__(
        self,
        name: str,
        inn: Optional[str] = None,
        ogrn: Optional[str] = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.inn = inn
        self.ogrn = ogrn
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()

    @classmethod
    def from_xml(cls, element: Element):
        """
        Создаёт объект Publisher из XML-элемента.

        :param element: XML-элемент <Publisher>
        :return: Экземпляр Publisher
        """
        name = element.findtext("Name")
        inn = element.findtext("Inn")
        ogrn = element.findtext("Ogrn")

        publisher = cls(name, inn, ogrn)

        return publisher

    def get_or_create(self, conn) -> int:
        """
        Ищет существующего издателя по OGRN или INN, либо создаёт нового в базе данных.

        :param conn: Соединение с базой данных SQLite
        :return: ID записи в базе данных
        """
        cursor = conn.cursor()

        # Проверка по OGRN (или INN, если OGRN нет)
        if self.ogrn:
            cursor.execute("SELECT id FROM publisher WHERE ogrn = ?", (self.ogrn,))
        elif self.inn:
            cursor.execute("SELECT id FROM publisher WHERE inn = ?", (self.inn,))
        else:
            raise ValueError("Не указан OGRN или INN для поиска/создания издателя")

        existing = cursor.fetchone()
        if existing:
            self.id = existing[0]
            return self.id

        cursor.execute(
            """
            INSERT INTO publisher (name, inn, ogrn, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (self.name, self.inn, self.ogrn, self.created_at, self.updated_at)
        )
        self.id = cursor.lastrowid

        conn.commit()
        return self.id