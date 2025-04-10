# main.py

from db_creator import create_database, create_tables
from data_loader import load_data
from db_manager import DBManager


def main():
    print("Создание базы данных и таблиц...")
    create_database()
    create_tables()

    print("Загрузка данных с hh.ru...")
    load_data()

    db = DBManager()

    while True:
        print("\nВыберите действие:")
        print("1 — Компании и кол-во вакансий")
        print("2 — Все вакансии")
        print("3 — Средняя зарплата")
        print("4 — Вакансии с ЗП выше средней")
        print("5 — Поиск по ключевому слову")
        print("0 — Выход")

        choice = input("Введите номер: ")

        if choice == "1":
            for name, count in db.get_companies_and_vacancies_count():
                print(f"{name}: {count} вакансий")
        elif choice == "2":
            for row in db.get_all_vacancies():
                print(row)
        elif choice == "3":
            print(f"Средняя зарплата: {db.get_avg_salary():.2f}")
        elif choice == "4":
            for row in db.get_vacancies_with_higher_salary():
                print(row)
        elif choice == "5":
            keyword = input("Введите ключевое слово: ")
            for row in db.get_vacancies_with_keyword(keyword):
                print(row)
        elif choice == "0":
            print("До свидания!")
            db.close()
            break
        else:
            print("Неверный ввод. Попробуйте ещё раз.")


if __name__ == "__main__":
    main()
