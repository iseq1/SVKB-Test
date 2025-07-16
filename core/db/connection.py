"""
Функции управления БД
"""
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "extrajudicial.db")
SQL_SCHEMA_PATH = os.path.join(os.path.join(BASE_DIR, "db"), "schema.sql")


def get_connection() -> sqlite3.Connection:
    """
    Создает и возвращает подключение к базе данных SQLite.

    :return: Объект подключения sqlite3.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> str:
    """
    Инициализирует базу данных, выполняя SQL-скрипт со схемой.

    :return: Абсолютный путь к инициализированной базе данных.
    """
    conn = get_connection()
    with open(SQL_SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    return DB_PATH
