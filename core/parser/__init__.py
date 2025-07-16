from core.parser.extractor import extract_all_from_raw_dir
from core.parser.extractor import EXTRACTED_DIR
from core.utils.logger import get_logger
logger = get_logger(__name__)

def parse_main():
    """
    Запускает процесс распаковки и декодирования всех рабочих файлов из исходной директории.

    :return: Список путей к успешно распакованным XML-файлам, либо None при ошибке
    """

    logger.info(f"Начался процесс декодирования рабочих файлов")
    try:
        xml_paths = extract_all_from_raw_dir()
        logger.info(f"Все рабочие файлы ({len(xml_paths)} шт.) успешно декодированы и расположены по пути: \"{EXTRACTED_DIR}\"")
        return xml_paths
    except Exception as e:
        logger.error(f"Ошибка декодирования рабочих файлов: {e}")