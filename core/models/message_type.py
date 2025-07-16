"""

"""
from datetime import datetime
from typing import Optional
from xml.etree.ElementTree import Element


class MessageType:
    def __init__(
        self,
        code: str,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.code = code
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()

    @classmethod
    def from_xml(cls, element: Element):
        """
        Создаёт экземпляр MessageType из XML-элемента.

        :param element: XML-элемент, содержащий код типа сообщения.
        :return: Новый экземпляр MessageType.
        """

        return cls(code=element.text)

    def get_or_create(self, conn) -> int:
        """
        Проверяет наличие записи с таким кодом в БД.
        Если запись существует — возвращает её ID.
        Если не существует — создаёт новую и возвращает её ID.

        :param conn: Соединение с SQLite базой данных.
        :return: ID существующей или новой записи message_types.
        """

        cursor = conn.cursor()

        # Проверка на существование по коду
        cursor.execute("SELECT id FROM message_types WHERE code = ?", (self.code,))
        row = cursor.fetchone()

        if row:
            self.id = row[0]
        else:
            cursor.execute(
                """
                INSERT INTO message_types (code, created_at, updated_at)
                VALUES (?, ?, ?)
                """,
                (self.code, self.created_at, self.updated_at)
            )
            self.id = cursor.lastrowid
            conn.commit()

        return self.id
