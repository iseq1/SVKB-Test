"""

"""
def get_percentage_of_total_amount_paid(conn):
    """
    Получает данные по проценту погашения общей суммы задолженности для физических лиц.

    :param conn: Объект соединения с базой данных
    :return: Список записей с полями: имя физ.лица, ИНН и процент погашения
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 
            debtor.name AS "Имя физ.лица", 
            debtor.inn AS "ИНН физ.лица", 
            ROUND(
                (1 - SUM(monetary_obligations.debt_sum) / SUM(monetary_obligations.total_sum)) * 100, 2
            ) AS "Процент погашения"
        FROM extrajudicial_bankruptcy_message
        JOIN debtor ON extrajudicial_bankruptcy_message.debtor_id = debtor.id
        JOIN creditors_non_from_entrepreneurship ON extrajudicial_bankruptcy_message.id = creditors_non_from_entrepreneurship.message_id
        JOIN monetary_obligations ON creditors_non_from_entrepreneurship.id = monetary_obligations.creditor_non_id
        WHERE monetary_obligations.total_sum > 0 AND monetary_obligations.total_sum IS NOT NULL
        GROUP BY debtor.id
        HAVING SUM(monetary_obligations.total_sum) > 0
        ORDER BY "Процент погашения" ASC
        """
    )
    return cursor.fetchall()


def print_percentage_of_total_amount_paid(conn):
    """
    Выводит в консоль таблицу с физическими лицами и их процентом погашенной задолженности.

    :param conn: Объект соединения с базой данных
    :return: None
    """

    rows = get_percentage_of_total_amount_paid(conn)

    print("Физические лица с процентом общей выплаченной суммы:")
    print("." + "_" * 60 + ".")
    print("| {:^12} | {:^15} | {:^20} |".format("Имя физ.лица", "ИНН физ.лица", "Общая сумма задолженности"))
    print("|" + "-" * 14 + "|" + "-" * 17 + "|" + "-" * 27 + "|")

    for row in rows:
        value = row["Процент погашения"]

        print(
            "| {:^12} | {:^15} | {:^25} |".format(
                row["Имя физ.лица"] or "—",
                row["ИНН физ.лица"] or "—",
                "-" if value is None else f"{value:.2f} %"
            )
        )