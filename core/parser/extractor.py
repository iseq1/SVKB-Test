from pathlib import Path
from typing import Optional, List
from core.parser.extractor_plugins import EXTRACTION_PLUGINS
from core.utils.logger import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
EXTRACTED_DIR = BASE_DIR / "data" / "extracted"
EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)


def extract_single_file(file_path: Path) -> Optional[Path]:
    """
    Распаковывает один архивный файл с помощью подходящего плагина.

    :param file_path: Путь к архивному файлу
    :return: Путь к распакованному XML-файлу или None, если распаковка не удалась
    """

    suffix = file_path.suffix
    plugin = EXTRACTION_PLUGINS.get(suffix)

    if not plugin:
        logger.warning(f"Неподдерживаемый формат: {file_path.name}")
        return None

    out_path = EXTRACTED_DIR / file_path.with_suffix("").name
    if out_path.exists():
        logger.info(f"Пропущен (уже распакован): {file_path.name}")
        return out_path

    try:
        extracted = plugin(file_path, EXTRACTED_DIR)
        if extracted:
            logger.info(f"Распакован {suffix}: {file_path.name} → {extracted.name}")
        else:
            logger.warning(f"Файл не распакован: {file_path.name}")
        return extracted
    except Exception as e:
        logger.error(f"Ошибка при распаковке {file_path.name}: {e}")
        return None


def extract_all_from_raw_dir() -> List[Path]:
    """
    Обходит директорию с сырыми файлами и распаковывает все поддерживаемые архивы.

    :return: Список путей ко всем успешно распакованным XML-файлам
    """

    extracted = []
    for path in RAW_DIR.iterdir():
        if path.suffix in EXTRACTION_PLUGINS:
            result = extract_single_file(path)
            if result:
                extracted.append(result)
    return extracted
