from core.services import initialize_models_from_xml
from core.db import initialize_database
from core.utils.logger import get_logger
from core.parser import parse_main
from core.sql.queries import init_sql_tasks
from core.visualization.fabric import init_view_tasks
logger = get_logger(__name__)


def create_app():
    """
    Основная функция приложения, которая:

    - инициализирует базу данных,
    - парсит и обрабатывает XML файлы,
    - инициализирует модели и записывает данные в БД,
    - запускает SQL-запросы для аналитики,
    - инициализирует построение визуализаций.

    В случае ошибки логирует её, а также сообщает об успешном завершении процесса.
    """

    try:
        logger.info(f"Основной процесс инициализирован")
        initialize_database()
        xml_paths = parse_main()
        initialize_models_from_xml(xml_paths)
        init_sql_tasks()
        init_view_tasks()
    except Exception as e:
        logger.error(f"Основной процесс столкнулся с ошибкой: {e}")
    finally:
        logger.info(f"Основной процесс успешно завершен")

