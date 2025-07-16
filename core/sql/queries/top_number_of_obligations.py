"""

"""
def get_top_ten_number_of_obligations(conn):
    """
    Получает ТОП-10 физических лиц по количеству их обязательств.

    :param conn: Объект соединения с базой данных
    :return: Список кортежей с данными (имя, ИНН, количество обязательств)
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 
            debtor.name AS "Имя физ.лица", 
            debtor.inn AS "ИНН физ.лица", 
            COUNT(monetary_obligations.id) AS "Кол-во обязательств" 
        FROM extrajudicial_bankruptcy_message
        JOIN debtor ON extrajudicial_bankruptcy_message.debtor_id = debtor.id
        JOIN creditors_non_from_entrepreneurship ON extrajudicial_bankruptcy_message.id = creditors_non_from_entrepreneurship.message_id
        JOIN monetary_obligations ON creditors_non_from_entrepreneurship.id = monetary_obligations.creditor_non_id
        GROUP BY debtor.id
        ORDER BY COUNT(monetary_obligations.id) DESC
        LIMIT 10
        """
    )
    return cursor.fetchall()


def print_top_ten_number_of_obligations(conn):
    """
    Выводит в консоль таблицу с ТОП-10 физических лиц по количеству обязательств.

    :param conn: Объект соединения с базой данных
    :return: None
    """

    rows = get_top_ten_number_of_obligations(conn)

    print("ТОП 10 физических лиц по количеству обязательств:")
    print("_" * 57)
    print("| {:^12} | {:^15} | {:^20} |".format("Имя физ.лица", "ИНН физ.лица", "Кол-во обязательств"))
    print("|" + "-" * 14 + "|" + "-" * 17 + "|" + "-" * 22 + "|")

    for row in rows:
        print(
            "| {:^12} | {:^15} | {:^20} |".format(
                row["Имя физ.лица"],
                row["ИНН физ.лица"],
                row["Кол-во обязательств"]
            )
        )