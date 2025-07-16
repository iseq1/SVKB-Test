"""

"""
def get_amount_of_debts_by_region(conn):
    """
    Получает суммарную сумму задолженностей физических лиц, сгруппированную по регионам.

    :param conn: Объект соединения с базой данных
    :return: Список кортежей с регионами и общей суммой задолженностей в каждом регионе
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 
            address.region AS region, 
            SUM(monetary_obligations.debt_sum) AS total_debt 
        FROM extrajudicial_bankruptcy_message
        JOIN debtor ON extrajudicial_bankruptcy_message.debtor_id = debtor.id
        JOIN creditors_non_from_entrepreneurship ON extrajudicial_bankruptcy_message.id = creditors_non_from_entrepreneurship.message_id
        JOIN monetary_obligations ON creditors_non_from_entrepreneurship.id = monetary_obligations.creditor_non_id
        JOIN address ON debtor.id = address.debtor_id
        WHERE monetary_obligations.debt_sum IS NOT NULL
        GROUP BY region
        ORDER BY total_debt DESC
        """
    )
    return cursor.fetchall()