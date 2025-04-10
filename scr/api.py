# api.py

import requests


def get_employer_info(employer_id: str) -> dict:
    """Получает информацию о работодателе по ID с hh.ru"""
    url = f"https://api.hh.ru/employers/{employer_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_vacancies_by_employer(employer_id: str, employer_name: str) -> list[dict]:
    """Получает вакансии работодателя по ID и выводит прогресс с названием компании"""
    vacancies = []
    page = 0
    max_pages = 10  # только 10 страниц

    while page < max_pages:
        url = "https://api.hh.ru/vacancies"
        params = {
            "employer_id": employer_id,
            "page": page,
            "per_page": 100
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Ошибка при запросе вакансий от {employer_name}: {e}")
            break

        data = response.json()
        vacancies.extend(data.get("items", []))

        print(f"Загружена страница {page + 1} из 10 для работодателя '{employer_name}'")

        if page >= data.get("pages", 0) - 1:
            break

        page += 1

    return vacancies
