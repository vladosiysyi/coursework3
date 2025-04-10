from file_utils import load_from_json
from api import get_employer_info, get_vacancies_by_employer
from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
import psycopg2


def load_data():
    """
    Загружает данные о работодателях и их вакансиях, сохраняет их в базу данных.

    Этот метод:
    - Загружает список компаний из файла JSON.
    - Для каждой компании получает информацию о работодателе.
    - Вставляет данные о работодателе в таблицу `employers`.
    - Загружает вакансии для каждой компании и вставляет их в таблицу `vacancies`.

    Использует подключение к базе данных PostgreSQL через psycopg2.

    Raises:
        psycopg2.DatabaseError: Если возникает ошибка при взаимодействии с базой данных.
        requests.exceptions.RequestException: Если запросы к API hh.ru не удались.
    """
    companies = load_from_json("companies.json")

    # Подключение к базе данных
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    for company in companies:
        employer_id = company["id"]
        info = get_employer_info(employer_id)

        employer_name = info["name"]  # Получаем имя работодателя

        # Вставка работодателя
        cur.execute("""
            INSERT INTO employers (hh_id, name)
            VALUES (%s, %s)
            ON CONFLICT (hh_id) DO NOTHING
            RETURNING id
        """, (employer_id, employer_name))
        result = cur.fetchone()
        db_employer_id = result[0] if result else None

        if not db_employer_id:
            cur.execute("SELECT id FROM employers WHERE hh_id = %s", (employer_id,))
            db_employer_id = cur.fetchone()[0]

        # Вставка вакансий
        vacancies = get_vacancies_by_employer(employer_id, employer_name)  # Передаем имя работодателя
        for vacancy in vacancies:
            salary = vacancy["salary"] or {}
            cur.execute("""
                INSERT INTO vacancies (employer_id, title, salary_from, salary_to, url)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                db_employer_id,
                vacancy["name"],
                salary.get("from"),
                salary.get("to"),
                vacancy["alternate_url"]
            ))

    conn.commit()
    cur.close()
    conn.close()
