"""

"""
def get_top_ten_debt_sum_of_obligations(conn):
    """
    Получает ТОП-10 физических лиц с наибольшей общей суммой задолженности.

    :param conn: Объект соединения с базой данных
    :return: Список кортежей с данными (имя, ИНН, сумма задолженности)
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 
            debtor.name AS "Имя физ.лица", 
            debtor.inn AS "ИНН физ.лица", 
            SUM(monetary_obligations.debt_sum) AS "Общая сумма задолженности" 
        FROM extrajudicial_bankruptcy_message
        JOIN debtor ON extrajudicial_bankruptcy_message.debtor_id = debtor.id
        JOIN creditors_non_from_entrepreneurship ON extrajudicial_bankruptcy_message.id = creditors_non_from_entrepreneurship.message_id
        JOIN monetary_obligations ON creditors_non_from_entrepreneurship.id = monetary_obligations.creditor_non_id
        GROUP BY debtor.id
        ORDER BY SUM(monetary_obligations.debt_sum) DESC
        LIMIT 10
        """
    )
    return cursor.fetchall()


def print_top_ten_debt_sum(conn):
    """
    Выводит в консоль таблицу с ТОП-10 физических лиц по общей сумме задолженности.

    :param conn: Объект соединения с базой данных
    :return: None
    """

    rows = get_top_ten_debt_sum_of_obligations(conn)

    print("ТОП 10 физических лиц с наибольшей общей суммой задолженностей:")
    print("." + "_" * 60 + ".")
    print("| {:^12} | {:^15} | {:^20} |".format("Имя физ.лица", "ИНН физ.лица", "Общая сумма задолженности"))
    print("|" + "-" * 14 + "|" + "-" * 17 + "|" + "-" * 27 + "|")

    for row in rows:
        print(
            "| {:^12} | {:^15} | {:^25} |".format(
                row["Имя физ.лица"] or "—",
                row["ИНН физ.лица"] or "—",
                "{:,.2f}".format(row["Общая сумма задолженности"])
            )
        )