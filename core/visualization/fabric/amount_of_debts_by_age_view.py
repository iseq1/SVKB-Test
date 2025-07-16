import os

from core.sql.queries.amount_of_debts_by_age import get_amount_of_debts_by_age
import matplotlib.pyplot as plt


def plot_debt_by_age(conn):
    """
    Строит и сохраняет столбчатую диаграмму суммы задолженностей по возрастным группам.

    :param conn: Объект соединения с базой данных.
    """

    # Получение данных
    rows = get_amount_of_debts_by_age(conn)
    age_groups = [f"{int(row[0])}–{int(row[0])+9}" for row in rows]
    debts = [float(row[1]) for row in rows]

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.bar(age_groups, debts, color='skyblue')
    plt.xlabel("Возрастная группа")
    plt.ylabel("Сумма задолженности")
    plt.title("Задолженность по возрастным группам физических лиц")
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    # Сохранение графика
    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, "debt_by_age.png"), dpi=300)

    plt.show()
