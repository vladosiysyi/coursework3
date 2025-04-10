# db_manager.py
import psycopg2
from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        self.cur.execute("""
            SELECT e.name, COUNT(v.id)
            FROM employers e
            LEFT JOIN vacancies v ON e.id = v.employer_id
            GROUP BY e.name
        """)
        return self.cur.fetchall()

    def get_all_vacancies(self, keyword: str = '') -> list[tuple]:
        self.cur.execute("""
            SELECT employers.name, vacancies.title, vacancies.salary_from, vacancies.salary_to, vacancies.url
            FROM vacancies
            JOIN employers ON employers.id = vacancies.employer_id
            WHERE vacancies.title LIKE %s
        """, (f"%{keyword}%",))
        return self.cur.fetchall()

    def get_avg_salary(self) -> float:
        self.cur.execute("""
            SELECT AVG(
                CASE
                    WHEN salary_from IS NOT NULL AND salary_to IS NOT NULL THEN (salary_from + salary_to) / 2
                    WHEN salary_from IS NOT NULL THEN salary_from
                    WHEN salary_to IS NOT NULL THEN salary_to
                    ELSE NULL
                END)
            FROM vacancies
            WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
        """)
        return self.cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        avg = self.get_avg_salary()
        self.cur.execute("""
            SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.id
            WHERE COALESCE(salary_from + salary_to, salary_from, salary_to) > %s
        """, (avg,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        self.cur.execute("""
            SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.id
            WHERE v.title ILIKE %s
        """, (f"%{keyword}%",))
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()
