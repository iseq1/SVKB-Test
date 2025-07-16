"""

"""
from datetime import datetime
from typing import Optional, List
from xml.etree.ElementTree import Element
from core.models.address import Address
from core.models.previous_name import PreviousName

class Debtor:
    def __init__(
        self,
        name: str,
        birth_date: Optional[str] = None,
        birth_place: Optional[str] = None,
        inn: Optional[str] = None,
        snils: Optional[str] = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.birth_date = birth_date
        self.birth_place = birth_place
        self.inn = inn
        self.snils = snils
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()

        self.address: Optional[Address] = None
        self.previous_names: List[PreviousName] = []


    @classmethod
    def from_xml(cls, element: Element):
        """
        Создаёт экземпляр Debtor из XML-элемента.

        Извлекает основные поля должника, а также связанные объекты:
        адрес и предыдущие имена (NameHistory).

        :param element: XML-элемент с данными должника.
        :return: Экземпляр Debtor.
        """

        name = element.findtext("Name")
        birth_date = element.findtext("BirthDate")
        birth_place = element.findtext("BirthPlace")
        inn = element.findtext("Inn")
        snils = element.findtext("Snils")

        debtor = cls(name, birth_date, birth_place, inn, snils)

        # Парсим Address
        address_el = element.find("Address")
        if address_el is not None:
            from core.models.address import Address
            debtor.address = Address.from_xml(address_el)

        # Парсим PreviousName
        name_history_el = element.find("NameHistory")
        if name_history_el is not None:
            from core.models.previous_name import PreviousName
            for prev_el in name_history_el.findall("PreviousName"):
                value = prev_el.findtext("Value")
                if value:
                    debtor.previous_names.append(PreviousName(value=value))

        return debtor

    def create(self, conn) -> int:
        """
        Сохраняет должника и связанные с ним данные в базе.

        Вставляет запись в таблицу debtor, а также
        добавляет адрес и связи с предыдущими именами.

        :param conn: Соединение с базой данных SQLite.
        :return: ID созданной записи должника.
        """

        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO debtor (name, birth_date, birth_place, inn, snils, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (self.name, self.birth_date, self.birth_place,
            self.inn, self.snils, self.created_at, self.updated_at)
        )
        self.id = cursor.lastrowid

        # Вставка Address
        if self.address:
            self.address.debtor_id = self.id
            self.address.create(conn)

        # Вставка PreviousNames
        for prev_name in self.previous_names:
            prev_name_id = prev_name.get_or_create(conn)
            cursor.execute(
                """
                INSERT OR IGNORE INTO debtor_previous_name (
                    debtor_id, previous_name_id, created_at, updated_at
                ) VALUES (?, ?, ?, ?)
                """,
                (self.id, prev_name_id, self.created_at, self.updated_at)
            )

        conn.commit()
        return self.id

    def get_existing_id(self, conn):
        """
        Проверяет наличие должника в базе по ИНН.

        :param conn: Соединение с базой данных SQLite.
        :return: ID должника, если найден, иначе None.
        """

        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM debtor WHERE inn = ?", (self.inn,)
        )
        result = cursor.fetchone()
        return result["id"] if result else None
