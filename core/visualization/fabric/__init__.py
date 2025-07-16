from core.db.connection import get_connection
from core.utils.logger import get_logger
from core.visualization.fabric.amount_of_debts_by_age_view import plot_debt_by_age
from core.visualization.fabric.amount_of_debts_by_region_view import plot_debt_by_region

logger = get_logger(__name__)


def init_view_tasks():
    """
    Инициализирует процесс построения визуализаций аналитики по обязательствам физических лиц
    """

    conn = get_connection()
    try:
        logger.info(f"Процесс построения аналитики по обязательствам физ.лиц инициализирован")
        plot_debt_by_region(conn)
        plot_debt_by_age(conn)

    except Exception as e:
        logger.error(f"Произошла ошибка при построении аналитики по обязательствам физ.лиц: {e}")
    finally:
        conn.close()
        logger.info(f"Процесс построения аналитики по обязательствам физ.лиц успешно завершен")

