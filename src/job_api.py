from abc import ABC, abstractmethod
from typing import Any, Dict, List


class JobAPI(ABC):
    """Абстрактный класс для работы с API сервисов с вакансиями"""

    @abstractmethod
    def __init__(self) -> None:
        """Инициализация класса для работы с API"""
        pass

    @abstractmethod
    def connect(self) -> None:
        """Подключение к API"""
        pass

    @abstractmethod
    def get_vacancies(self, search_query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        Получение списка вакансий по поисковому запросу
        :param search_query: Поисковый запрос
        :param kwargs: Дополнительные параметры запроса
        :return: Список словарей с данными о вакансиях
        """
        pass
