import re
from typing import Dict

def normalize_address_str(addr: str) -> str:
    """
    Нормализует строку адреса: заменяет сокращения, вставляет запятые, убирает лишние пробелы.

    :param addr: Входная строка адреса
    :return: Нормализованная строка адреса
    """
    addr = addr.strip()

    # Список ключевых замен
    replacements = [
        (r"\bобл\.", "область, "),
        (r"\bобл\b.", "область, "),
        (r"\bр-н\b", "район, "),
        (r"\bгор\.?", "город "),
        (r"\bг\.", "город "),
        (r"\bг\b", "город "),
        (r"\bс\.", "село "),
        (r"\bд\.", "дом "),
        (r"\bд\b", "дом "),
        (r"\bкв\.", "квартира "),
        (r"\bкв\b", "квартира "),
        (r"\bпгт\.?", "поселок городского типа "),
        (r"\bрп\.?\b", "рабочий поселок "),
        (r"(?<![а-яА-ЯёЁ])ул\.?(?![а-яА-ЯёЁ])", "улица "),
        (r"\bпр-?т\.?", "проспект "),
        (r"\bпер\.?", "переулок "),
        (r"\bмкр\.?", "микрорайон "),
        (r"\респ\b", "республика "),
        (r"\тер\.", "территория "),
    ]

    for pattern, replacement in replacements:
        addr = re.sub(pattern, replacement, addr, flags=re.IGNORECASE)
    # Теперь вставим запятую между стыкованными словами (если пропущена)
    addr = re.sub(r"(?<=[а-яА-ЯёЁ])(?=\b(область|район|город|деревня|рабочий поселок|поселок|село|улица|проспект|переулок|дом|квартира))", ", ", addr, flags=re.IGNORECASE)
    addr = re.sub(r'(?<![,])\s+(улица|дом|квартира)\b', r', \1', addr, flags=re.IGNORECASE)

    # Удалим лишние пробелы и запятые
    addr = re.sub(r",\s*,", ", ", addr)
    addr = re.sub(r"\s{2,}", " ", addr)

    return addr.strip()

def parse_address(addr: str) -> Dict[str, str]:
    """
    Парсит нормализованную строку адреса, выделяя ключевые части: индекс, регион, район, населённый пункт, улицу, дом, квартиру.

    :param addr: Нормализованная строка адреса
    :return: Словарь с компонентами адреса (postal_code, region, district, settlement, street, building, apartment)
    """

    result = {
        "postal_code": None,
        "region": None,
        "district": None,
        "settlement": None,
        "street": None,
        "building": None,
        "apartment": None,
    }

    patterns = {
        "postal_code": r"\b(\d{6})\b",
        "region": r"(Республика\s[А-ЯЁа-яё\- ]+|[А-ЯЁа-яё\- ]+(?:область|край|республика))",
        "district": r"([А-ЯЁа-яё\s\-]+ район)",
        "settlement": r"(город|рабочий поселок|село|деревня|поселок(?: городского типа)?)[\s\-]+([А-ЯЁа-яё0-9\s\-]+)",
        "street": r"(улица|территория|проспект|переулок|микрорайон)[\s\-]+([А-ЯЁа-яё0-9\s\-\/]+)",
        "building": r"дом[\s№]*([\d]+(?:[/\-]\d+)?[а-яА-Я]?)",
        "apartment": r"квартира[\s№]*([0-9]+)",
    }

    addr = normalize_address_str(addr)
    for key, pattern in patterns.items():
        match = re.search(pattern, addr, re.IGNORECASE)
        if match:
            if key in ["settlement", "street"]:
                result[key] = f"{match.group(1).capitalize()} {match.group(2).strip()}"
            else:
                result[key] = match.group(1).strip().capitalize()

    return result


# raw = "Орловская обл, Троснянский р-н, д. Саковнинки, д. 7"
#
#
# parsed = parse_address(raw)
# print(parsed)