import os
import tempfile
from src.utils import (
    filter_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies,
    save_vacancies_to_file
)

# Тестовые данные
TEST_VACANCIES = [
    {
        'name': 'Python Developer',
        'url': 'https://hh.ru/vacancy/1',
        'salary_from': 100000,
        'salary_to': 150000,
        'salary_currency': 'RUR',
        'description': 'Опыт работы с Python от 3 лет',
        'employer': 'Test Company',
        'experience': 'От 3 до 6 лет',
        'employment': 'Полная занятость'
    },
    {
        'name': 'Senior Python Developer',
        'url': 'https://hh.ru/vacancy/2',
        'salary_from': 200000,
        'salary_to': 300000,
        'salary_currency': 'RUR',
        'description': 'Опыт работы с Python от 5 лет, Django, Flask',
        'employer': 'Another Company',
        'experience': 'От 5 лет',
        'employment': 'Полная занятость'
    },
    {
        'name': 'Junior Python Developer',
        'url': 'https://hh.ru/vacancy/3',
        'salary_from': 50000,
        'salary_to': 80000,
        'salary_currency': 'RUR',
        'description': 'Базовые знания Python',
        'employer': 'Startup',
        'experience': 'Нет опыта',
        'employment': 'Полная занятость'
    }
]


def test_filter_vacancies():
    """Тест фильтрации вакансий по ключевым словам"""
    # Фильтрация по одному слову
    filtered = filter_vacancies(TEST_VACANCIES, ['Senior'])
    assert len(filtered) == 1
    assert filtered[0]['name'] == 'Senior Python Developer'

    # Фильтрация по нескольким словам
    filtered = filter_vacancies(TEST_VACANCIES, ['Python', 'Django'])
    assert len(filtered) == 1
    assert filtered[0]['name'] == 'Senior Python Developer'

    # Без ключевых слов - возвращаются все вакансии
    filtered = filter_vacancies(TEST_VACANCIES, [])
    assert len(filtered) == 3


def test_get_vacancies_by_salary():
    """Тест фильтрации по зарплате"""
    # Диапазон, подходящий для всех
    filtered = get_vacancies_by_salary(TEST_VACANCIES, '0-1000000')
    assert len(filtered) == 3

    # Только Senior попадает в диапазон
    filtered = get_vacancies_by_salary(TEST_VACANCIES, '200000-400000')
    assert len(filtered) == 1
    assert filtered[0]['name'] == 'Senior Python Developer'

    # Некорректный диапазон - возвращаются все
    filtered = get_vacancies_by_salary(TEST_VACANCIES, 'некорректный-формат')
    assert len(filtered) == 3


def test_sort_vacancies():
    """Тест сортировки вакансий"""
    # Создаем копию, чтобы не менять исходные данные
    vacancies = TEST_VACANCIES.copy()

    # Сортируем по убыванию зарплаты
    sorted_vacancies = sort_vacancies(vacancies)

    # Проверяем порядок
    assert sorted_vacancies[0]['name'] == 'Senior Python Developer'
    assert sorted_vacancies[1]['name'] == 'Python Developer'
    assert sorted_vacancies[2]['name'] == 'Junior Python Developer'

    # Проверяем, что исходный список не изменился
    assert vacancies == TEST_VACANCIES


def test_get_top_vacancies():
    """Тест получения N первых вакансий"""
    # Берем 2 вакансии из 3
    top = get_top_vacancies(TEST_VACANCIES, 2)
    assert len(top) == 2
    assert top[0]['name'] == 'Python Developer'
    assert top[1]['name'] == 'Senior Python Developer'

    # Если запросили больше, чем есть
    top = get_top_vacancies(TEST_VACANCIES, 10)
    assert len(top) == 3


def test_save_vacancies_to_file():
    """Тест сохранения вакансий в файл"""
    # Создаем временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as temp_file:
        temp_path = temp_file.name

    try:
        # Сохраняем вакансии
        save_vacancies_to_file(TEST_VACANCIES, temp_path)

        # Проверяем, что файл создан и не пустой
        assert os.path.exists(temp_path)
        assert os.path.getsize(temp_path) > 0

    finally:
        # Удаляем временный файл
        if os.path.exists(temp_path):
            os.unlink(temp_path)