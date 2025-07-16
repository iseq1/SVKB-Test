from xml.etree import ElementTree as ET
from core.db.connection import get_connection
from core.models.extrajudicial_bankruptcy_message import ExtrajudicialBankruptcyMessage
from core.utils.logger import get_logger
logger = get_logger(__name__)

def initialize_models_from_xml(xml_paths: list[str]):
    """
    Парсит список XML-файлов, извлекает сообщения, связанные модели, и сохраняет их в базу данных.

    Для каждого сообщения:
    - Проверяет и при необходимости создает запись должника (debtor) в БД.
    - Создает запись сообщения, если она еще не существует.

    :param xml_paths: Список путей к XML-файлам для обработки
    :return: None
    """

    conn = get_connection()
    try:
        total = 0
        logger.info(f"Начался процесс парсинга рабочих файлов и записи данных в БД")
        for path in xml_paths:
            logger.info(f"Обработка XML файла: \"{path}\"")
            tree = ET.parse(path)
            root = tree.getroot()

            for msg_el in root.findall("ExtrajudicialBankruptcyMessage"):
                message = ExtrajudicialBankruptcyMessage.from_xml(msg_el)

                if message.debtor:
                    existing_debtor_id = message.debtor.get_existing_id(conn)
                    if existing_debtor_id:
                        message.debtor_id = existing_debtor_id
                    else:
                        message.debtor_id = message.debtor.create(conn)

                if not message.exists(conn):
                    message.create(conn)
                    total += 1

            logger.info(f"Парсинг файла \"{path}\" успешно завершен, записей в БД = {total} шт.")


    except Exception as e:
        logger.error(f"Произошла ошибка при парсинге и сохранении данных в БД: {e}")
    finally:
        conn.close()
        logger.info(f"Процесс парсинга рабочих файлов и записи данных в БД успешно завершен!")
