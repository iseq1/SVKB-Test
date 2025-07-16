from core.db.connection import get_connection
from core.sql.queries.percentage_of_the_total_amount_paid import print_percentage_of_total_amount_paid
from core.sql.queries.top_debt_sum_of_obligations import print_top_ten_debt_sum
from core.sql.queries.top_number_of_obligations import print_top_ten_number_of_obligations
from core.utils.logger import get_logger
logger = get_logger(__name__)


def init_sql_tasks():
    """
    Выполняет последовательный запуск функций, которые выводят ключевые статистические данные по обязательствам физических лиц из базы данных.

    :return: None
    """

    conn = get_connection()

    try:
        logger.info(f"Процесс получения информации по обязательствам физ.лиц инициализирован")
        print_top_ten_number_of_obligations(conn)
        print_top_ten_debt_sum(conn)
        print_percentage_of_total_amount_paid(conn)

    except Exception as e:
        logger.error(f"Произошла ошибка при получения информации по обязательствам физ.лиц: {e}")
    finally:
        conn.close()
        logger.info(f"Процесс получения информации по обязательствам физ.лиц успешно завершен")
