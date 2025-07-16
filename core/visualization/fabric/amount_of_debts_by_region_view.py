import os

from core.sql.queries.amount_of_debts_by_region import get_amount_of_debts_by_region
import matplotlib.pyplot as plt


def plot_debt_by_region(conn):
    """
    Строит и сохраняет столбчатую диаграмму суммы задолженностей по регионам.

    :param conn: Объект соединения с базой данных.
    """

    # Получение данных
    rows = get_amount_of_debts_by_region(conn)
    regions = [row["region"] or "Неизвестно" for row in rows]
    debts = [row["total_debt"] for row in rows]

    # Построение графика
    plt.figure(figsize=(12, 6))
    plt.bar(regions, debts, color='steelblue')
    plt.xlabel("Регионы")
    plt.ylabel("Сумма задолженности")
    plt.title("Сумма задолженностей по регионам")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    # Сохранение графика
    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, "debt_by_region.png"), dpi=300)

    plt.show()
