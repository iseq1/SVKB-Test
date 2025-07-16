"""
Инициализирующий скрипт БД
"""
from core.db.connection import init_db
from core.utils.logger import get_logger

logger = get_logger(__name__)

def initialize_database() -> None:
    """
    Инициализирующий скрипт базы данных

    :return: None
    """
    logger.info(f"Начался процесс инициализации БД")
    try:
        db_name = init_db()
        logger.info(f"База данных \"{db_name}\" успешно инициализирована!")
    except Exception as e:
        logger.error(f"Ошибка инициализации БД: {e}")