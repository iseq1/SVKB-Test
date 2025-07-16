import xml.etree.ElementTree as ET
from collections import defaultdict
import sys

def collect_structures(xml_path):
    """
    Собирает структуру XML-документа в виде словаря,
    где ключ — путь до элемента, а значение — множество тегов его дочерних элементов.

    :param xml_path: Путь к XML-файлу для анализа
    :return: defaultdict(set), описывающий вложенность и поля элементов
    """

    tree = ET.parse(xml_path)
    root = tree.getroot()

    structure = defaultdict(set)

    def walk(elem, path=""):
        tag = elem.tag
        full_path = f"{path}/{tag}" if path else tag

        # Собираем поля текущего элемента
        for child in elem:
            structure[full_path].add(child.tag)
            walk(child, full_path)

    walk(root)
    return structure


def print_structures(structure):
    """
    Выводит на экран структуру XML в удобочитаемом формате.

    :param structure: Словарь, описывающий структуру XML (путь -> поля)
    :return: None
    """

    print("== Уникальные объекты и их поля ==")
    for obj_path in sorted(structure.keys()):
        print(f"\n {obj_path}")
        for field in sorted(structure[obj_path]):
            print(f"  └── {field}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_structure.py <path_to_xml>")
        sys.exit(1)

    xml_path = sys.argv[1]

