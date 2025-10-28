import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from .models import Vacancy


class Storage(ABC):
    """Абстрактный класс для работы с хранилищем данных"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в хранилище"""
        pass

    @abstractmethod
    def get_vacancies(self, **criteria) -> List[Dict[str, Any]]:
        """Получение списка вакансий по критериям"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: str) -> None:
        """Удаление вакансии по ID"""
        pass


class JSONStorage(Storage):
    """Класс для работы с JSON-файлом"""

    def __init__(self, filename: str = 'vacancies.json'):
        """
        Инициализация хранилища
        :param filename: Имя файла для хранения данных
        """
        self._filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Проверяет существование файла и создает его при необходимости"""
        try:
            with open(self._filename, 'a+', encoding='utf-8'):
                pass
        except IOError as e:
            raise IOError(f"Ошибка при работе с файлом {self._filename}: {e}")

    def _read_file(self) -> List[Dict[str, Any]]:
        """Чтение данных из файла"""
        try:
            with open(self._filename, 'r', encoding='utf-8') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []
        except FileNotFoundError:
            return []

    def _write_file(self, data: List[Dict[str, Any]]) -> None:
        """Запись данных в файл"""
        with open(self._filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в файл"""
        if not isinstance(vacancy, Vacancy):
            raise ValueError("Можно добавлять только объекты класса Vacancy")

        vacancies = self._read_file()
        vacancy_dict = vacancy.to_dict()

        # Генерируем ID, если его нет
        if 'id' not in vacancy_dict:
            import uuid
            vacancy_dict['id'] = str(uuid.uuid4())

        # Проверка на дубликаты по URL
        if not any(v.get('url') == vacancy.url for v in vacancies):
            vacancies.append(vacancy_dict)
            self._write_file(vacancies)

    def get_vacancies(self, **criteria: Any) -> List[Dict[str, Any]]:
        """
        Получение списка вакансий по критериям
        :param criteria: Ключевые слова для фильтрации (поле: значение)
        :return: Список словарей с данными о вакансиях
        """
        vacancies = self._read_file()

        if not criteria:
            return vacancies

        filtered_vacancies = []
        for vacancy in vacancies:
            match = True
            for key, value in criteria.items():
                if key not in vacancy or vacancy[key] != value:
                    match = False
                    break
            if match:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy(self, vacancy_id: str) -> None:
        """
        Удаление вакансии по ID
        :param vacancy_id: ID вакансии для удаления
        """
        vacancies = self._read_file()
        initial_count = len(vacancies)
        vacancies = [v for v in vacancies if v.get('id') != vacancy_id]

        if len(vacancies) < initial_count:
            self._write_file(vacancies)
        else:
            raise ValueError(f"Вакансия с ID {vacancy_id} не найдена")
