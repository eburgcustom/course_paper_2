from typing import Any, Dict, List

import requests

from src.job_api import JobAPI


class HeadHunterAPI(JobAPI):
    """Класс для взаимодействия с API hh.ru"""

    __base_url = "https://api.hh.ru/vacancies"
    __connected = False

    def __init__(self):
        """Инициализация класса для работы с API hh.ru"""
        super().__init__()
        self.connect()

    def connect(self) -> None:
        """Подключение к API hh.ru"""
        try:
            response = requests.get(self.__base_url, timeout=5)
            if response.status_code != 200:
                raise ConnectionError(f"Ошибка подключения к hh.ru: {response.status_code}")
            self.__connected = True
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Ошибка подключения к hh.ru: {str(e)}")

    def get_vacancies(self, search_query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        Получение списка вакансий по поисковому запросу
        :param search_query: Поисковый запрос
        :param kwargs: Дополнительные параметры запроса
        :return: Список словарей с данными о вакансиях
        """
        if not self.__connected:
            self.connect()

        params = {
            "text": search_query,
            "per_page": kwargs.get('per_page', 100),  # Максимальное количество результатов на странице
            "area": 113,  # Код России
            "only_with_salary": kwargs.get('only_with_salary', False),
            "page": kwargs.get('page', 0)
        }

        try:
            response = requests.get(self.__base_url, params=params, timeout=10)
            response.raise_for_status()

            vacancies = response.json().get("items", [])
            result = []

            for v in vacancies:
                salary = v.get("salary")
                if salary:
                    salary_from = salary.get('from')
                    salary_to = salary.get('to')
                    salary_currency = salary.get('currency', 'RUR')
                else:
                    salary_from = salary_to = salary_currency = None

                result.append({
                    "id": v.get("id"),
                    "name": v.get("name"),
                    "url": v.get("alternate_url"),
                    "salary_from": salary_from,
                    "salary_to": salary_to,
                    "salary_currency": salary_currency,
                    "description": v.get("snippet", {}).get("requirement", ""),
                    "employer": v.get("employer", {}).get("name"),
                    "experience": v.get("experience", {}).get("name"),
                    "employment": v.get("employment", {}).get("name")
                })

            return result

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Ошибка при получении вакансий: {str(e)}")
