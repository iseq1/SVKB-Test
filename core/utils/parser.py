from typing import Optional

def parse_float(value: Optional[str]) -> Optional[float]:
    """
    Преобразует строковое значение в число с плавающей точкой.

    :param value: Строка, содержащая числовое значение, либо None.
    :return: Число с плавающей точкой, если преобразование успешно, иначе None.
    """

    try:
        return float(value)
    except (ValueError, TypeError):
        return None