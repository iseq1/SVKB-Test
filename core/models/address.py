"""

"""
from datetime import datetime
from xml.etree.ElementTree import Element
from typing import Optional
from core.parser.extractor_address import parse_address


class Address:
    def __init__(
        self,
        full_address: str,
        postal_code: Optional[str] = None,
        region: Optional[str] = None,
        district: Optional[str] = None,
        settlement: Optional[str] = None,
        street: Optional[str] = None,
        building: Optional[str] = None,
        apartment: Optional[str] = None,
        debtor_id: Optional[int] = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.debtor_id = debtor_id
        self.full_address = full_address
        self.postal_code = postal_code
        self.region = region
        self.district = district
        self.settlement = settlement
        self.street = street
        self.building = building
        self.apartment = apartment
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()

    @classmethod
    def from_xml(cls, address_element: Element):
        """
        Создаёт экземпляр Address из XML-элемента.

        Извлекает полный адрес из текста элемента и парсит его на составные части.

        :param address_element: XML-элемент с адресом.
        :return: Экземпляр Address с заполненными полями.
        """

        full_address = address_element.text.strip() if address_element.text else ""

        result = parse_address(full_address)

        return cls(
            full_address=full_address,
            postal_code=result.get('postal_code', None),
            region=result.get('region', None),
            district=result.get('district', None),
            settlement=result.get('settlement', None),
            street=result.get('street', None),
            building=result.get('building', None),
            apartment=result.get('apartment', None),
        )

    def create(self, conn):
        """
        Вставляет адрес в базу данных.

        :param conn: Соединение с базой данных.
        """

        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO address (
                debtor_id, full_address, postal_code, region, district, settlement,
                street, building, apartment, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
            self.debtor_id, self.full_address, self.postal_code, self.region,
            self.district, self.settlement, self.street,
            self.building, self.apartment, self.created_at, self.updated_at
        ))
        self.id = cursor.lastrowid
        conn.commit()

