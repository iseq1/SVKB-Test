"""

"""
from datetime import datetime
from typing import Optional
from xml.etree.ElementTree import Element


class ExtrajudicialBankruptcyMessageBank:
    def __init__(
        self,
        message_id: str,
        bank_id: int,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.message_id = message_id
        self.bank_id = bank_id
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()

    @classmethod
    def from_xml(cls, element: Element, message_id: str):
        """
        Создаёт экземпляр ExtrajudicialBankruptcyMessageBank из XML-элемента.

        :param element: XML-элемент, содержащий информацию о банке.
        :param message_id: Идентификатор связанного сообщения о банкротстве.
        :return: Экземпляр ExtrajudicialBankruptcyMessageBank.
        """

        bank_id_text = element.findtext("Id")  # если у Bank внутри XML есть Id
        if not bank_id_text:
            raise ValueError("Bank Id not found in XML")
        return cls(message_id=message_id, bank_id=int(bank_id_text))

    def create(self, conn):
        """
        Сохраняет запись в таблице extrajudicial_bankruptcy_message_bank, если она ещё не существует.

        :param conn: Соединение с SQLite базой данных.
        """

        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR IGNORE INTO extrajudicial_bankruptcy_message_bank
            (message_id, bank_id, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            """,
            (self.message_id, self.bank_id, self.created_at, self.updated_at)
        )
        conn.commit()
