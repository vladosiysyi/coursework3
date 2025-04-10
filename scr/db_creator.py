# db_creator.py

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def create_database():
    """Создаёт базу данных, если она не существует"""
    conn = psycopg2.connect(
        dbname='postgres',
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
    exists = cur.fetchone()

    if not exists:
        cur.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"База данных '{DB_NAME}' создана.")
    else:
        print(f"База данных '{DB_NAME}' уже существует.")

    cur.close()
    conn.close()


def create_tables():
    """Создаёт таблицы employers и vacancies"""
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS employers (
            id SERIAL PRIMARY KEY,
            hh_id VARCHAR(20) UNIQUE NOT NULL,
            name TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            employer_id INTEGER REFERENCES employers(id) ON DELETE CASCADE,
            title TEXT NOT NULL,
            salary_from INTEGER,
            salary_to INTEGER,
            url TEXT
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
