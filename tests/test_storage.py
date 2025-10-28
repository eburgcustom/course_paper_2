import os
import tempfile

from src.models import Vacancy
from src.storage import JSONStorage


# Создаем временный файл для тестов
def create_temp_file():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    temp_file.close()
    return temp_file.name


# Фикстура для тестов
def setup_test_environment():
    temp_file = create_temp_file()
    storage = JSONStorage(temp_file)

    # Тестовые данные
    test_vacancy = Vacancy(
        name="Python Developer",
        url="http://example.com/vacancy/1",
        salary_from=100000,
        salary_to=150000,
        salary_currency="RUR"
    )

    test_vacancy_2 = Vacancy(
        name="Senior Python Developer",
        url="http://example.com/vacancy/2",
        salary_from=200000,
        salary_to=300000,
        salary_currency="RUR"
    )

    return storage, test_vacancy, test_vacancy_2, temp_file


def test_add_and_get_vacancies():
    """Тест добавления и получения вакансий"""
    storage, test_vacancy, test_vacancy_2, temp_file = setup_test_environment()

    try:
        # Добавляем вакансии
        storage.add_vacancy(test_vacancy)
        storage.add_vacancy(test_vacancy_2)

        # Получаем все вакансии
        vacancies = storage.get_vacancies()
        assert len(vacancies) == 2, "Должно быть 2 вакансии"

        # Проверяем данные первой вакансии
        assert vacancies[0]['name'] == "Python Developer"
        assert vacancies[0]['salary_from'] == 100000
        assert vacancies[1]['name'] == "Senior Python Developer"

    finally:
        # Очистка
        if os.path.exists(temp_file):
            os.unlink(temp_file)
