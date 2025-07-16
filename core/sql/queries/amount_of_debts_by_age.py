"""

"""
def get_amount_of_debts_by_age(conn):
    """
    Получает суммарную сумму задолженностей физических лиц, сгруппированную по возрастным группам с шагом 10 лет.

    :param conn: Объект соединения с базой данных
    :return: Список кортежей с возрастными группами и общей суммой задолженностей для каждой группы
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 
            (CAST((strftime('%Y', 'now') - strftime('%Y', debtor.birth_date)) / 10 AS INTEGER) * 10) AS age_group,
            SUM(monetary_obligations.debt_sum) AS total_debt
        FROM extrajudicial_bankruptcy_message
        JOIN debtor ON extrajudicial_bankruptcy_message.debtor_id = debtor.id
        JOIN creditors_non_from_entrepreneurship ON extrajudicial_bankruptcy_message.id = creditors_non_from_entrepreneurship.message_id
        JOIN monetary_obligations ON creditors_non_from_entrepreneurship.id = monetary_obligations.creditor_non_id
        WHERE monetary_obligations.debt_sum > 0
        GROUP BY age_group
        ORDER BY age_group;

        """
    )
    return cursor.fetchall()