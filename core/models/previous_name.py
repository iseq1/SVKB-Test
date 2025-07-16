"""
Модель PreviousName (предыдущее имя) для хранения истории переименований из XML.
"""
from datetime import datetime
from typing import Optional


class PreviousName:
    def __init__(
        self,
        value: str,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.value = value
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()

    @classmethod
    def from_xml(cls, element):
        """
        Создаёт объект PreviousName из XML-элемента.

        :param element: XML-элемент <PreviousName>.
        :return: Экземпляр PreviousName.
        """
        return cls(value=element.findtext("Value"))

    def get_or_create(self, conn) -> int:
        """
        Ищет запись с таким же значением в таблице `previous_name` или создаёт новую.

        :param conn: Соединение с базой данных SQLite.
        :return: ID найденной или созданной записи.
        """

        cursor = conn.cursor()

        # Проверка, есть ли уже такое имя
        cursor.execute("SELECT id FROM previous_name WHERE value = ?", (self.value,))
        row = cursor.fetchone()
        if row:
            self.id = row[0]
        else:
            cursor.execute("""
                INSERT INTO previous_name (value, created_at, updated_at)
                VALUES (?, ?, ?)
            """, (self.value, self.created_at, self.updated_at))
            self.id = cursor.lastrowid
            conn.commit()

        return self.id
