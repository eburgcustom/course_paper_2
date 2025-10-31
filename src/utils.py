import json
from typing import Any, Dict, List

from .models import Vacancy


def filter_vacancies(vacancies: List[Dict[str, Any]], filter_words: List[str]) -> List[Dict[str, Any]]:
    """
    Фильтрация вакансий по ключевым словам
    :param vacancies: Список вакансий
    :param filter_words: Список ключевых слов для фильтрации
    :return: Отфильтрованный список вакансий
    """
    if not filter_words:
        return vacancies

    filtered_vacancies = []
    for vacancy in vacancies:
        # Объединяем все текстовые поля для поиска
        text_to_search = ' '.join([
            str(vacancy.get('name', '')),
            str(vacancy.get('description', '')),
            str(vacancy.get('employer', '')),
            str(vacancy.get('experience', '')),
            str(vacancy.get('employment', ''))
        ]).lower()

        # Проверяем, содержатся ли все ключевые слова в тексте
        if all(word.lower() in text_to_search for word in filter_words):
            filtered_vacancies.append(vacancy)

    return filtered_vacancies


def get_vacancies_by_salary(vacancies: List[Dict[str, Any]], salary_range: str) -> List[Dict[str, Any]]:
    """
    Фильтрация вакансий по диапазону зарплат
    :param vacancies: Список вакансий
    :param salary_range: Строка с диапазоном зарплат в формате "min-max"
    :return: Отфильтрованный список вакансий
    """
    if not salary_range:
        return vacancies

    try:
        # Парсим диапазон зарплат
        salary_parts = salary_range.split('-')
        if len(salary_parts) != 2:
            return vacancies

        min_salary, max_salary = map(int, salary_parts)
    except (ValueError, IndexError):
        return vacancies

    filtered_vacancies = []
    for vacancy in vacancies:
        salary_from = vacancy.get('salary_from') or 0
        salary_to = vacancy.get('salary_to') or float('inf')

        # Проверяем пересечение диапазонов
        if (salary_from <= max_salary) and (salary_to >= min_salary):
            filtered_vacancies.append(vacancy)

    return filtered_vacancies


def sort_vacancies(vacancies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Сортировка вакансий по зарплате (по убыванию)
    :param vacancies: Список вакансий
    :return: Отсортированный список вакансий
    """
    def get_sort_key(vacancy) -> int:
        # Используем минимальную зарплату для сортировки
        salary_from = vacancy.get('salary_from') or 0
        salary_to = vacancy.get('salary_to') or 0
        # Если указана только максимальная зарплата, используем её
        if salary_from == 0 and salary_to > 0:
            return salary_to
        return max(salary_from, salary_to)

    return sorted(vacancies, key=get_sort_key, reverse=True)


def get_top_vacancies(vacancies: List[Dict[str, Any]], top_n: int) -> List[Dict[str, Any]]:
    """
    Получение топ N вакансий
    :param vacancies: Список вакансий
    :param top_n: Количество вакансий для вывода
    :return: Список из N лучших вакансий
    """
    return vacancies[:top_n] if top_n > 0 else vacancies


def print_vacancies(vacancies: List[Dict[str, Any]]) -> None:
    """
    Вывод списка вакансий в консоль
    :param vacancies: Список вакансий для вывода
    """
    if not vacancies:
        print("Вакансии не найдены.")
        return

    for i, vacancy_data in enumerate(vacancies, 1):
        vacancy = Vacancy.from_dict(vacancy_data)
        print(f"\nВакансия #{i}")
        print("-" * 50)
        print(vacancy)

    print(f"\nВсего найдено вакансий: {len(vacancies)}")


def save_vacancies_to_file(vacancies: List[Dict[str, Any]], filename: str = 'vacancies.json') -> None:
    """
    Сохранение списка вакансий в JSON-файл
    :param vacancies: Список вакансий
    :param filename: Имя файла для сохранения
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=2)
        print(f"\nДанные успешно сохранены в файл: {filename}")
    except IOError as e:
        print(f"\nОшибка при сохранении в файл: {e}")
