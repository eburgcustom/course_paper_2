from src.models import Vacancy


def test_vacancy_creation():
    """Тест создания вакансии"""
    vacancy = Vacancy(
        name='Python Developer',
        url='https://hh.ru/vacancy/12345',
        salary_from=100000,
        salary_to=150000,
        salary_currency='RUR',
        description='Требуется опытный Python разработчик',
        employer='ООО Тест',
        experience='От 3 до 6 лет',
        employment='Полная занятость'
    )
    assert vacancy.name == 'Python Developer'
    assert vacancy.url == 'https://hh.ru/vacancy/12345'
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 150000
    assert vacancy.salary_currency == 'RUR'
    assert vacancy.description == 'Требуется опытный Python разработчик'
    assert vacancy.employer == 'ООО Тест'
    assert vacancy.experience == 'От 3 до 6 лет'
    assert vacancy.employment == 'Полная занятость'


def test_salary_property():
    """Тест свойства salary"""
    # Полный диапазон зарплат
    vacancy = Vacancy('Test', 'https://test.com', 100000, 150000, 'RUR')
    assert vacancy.salary == '100 000 - 150 000 RUR'

    # Только зарплата "от"
    vacancy = Vacancy('Test', 'https://test.com', 100000, None, 'USD')
    assert vacancy.salary == 'от 100 000 USD'

    # Только зарплата "до"
    vacancy = Vacancy('Test', 'https://test.com', None, 200000, 'EUR')
    assert vacancy.salary == 'до 200 000 EUR'

    # Без зарплаты
    vacancy = Vacancy('Test', 'https://test.com')
    assert vacancy.salary == 'Зарплата не указана'


def test_comparison():
    """Тест сравнения вакансий"""
    v1 = Vacancy('Test1', 'https://test.com/1', 100000, 150000, 'RUR')
    v2 = Vacancy('Test2', 'https://test.com/2', 200000, 250000, 'RUR')
    v3 = Vacancy('Test1', 'https://test.com/1', 100000, 150000, 'RUR')

    # Проверка равенства
    assert v1 == v3
    assert v1 != v2

    # Проверка сравнения
    assert v2 > v1
    assert v1 < v2


def test_validation():
    """Тест валидации данных"""
    # Некорректный URL
    try:
        Vacancy('Test', 'invalid-url')
        assert False, "Должна быть ошибка валидации URL"
    except ValueError as e:
        assert "Некорректный URL" in str(e)

    # Некорректная зарплата
    try:
        Vacancy('Test', 'https://test.com', salary_from='не число')
        assert False, "Должна быть ошибка валидации зарплаты"
    except ValueError as e:
        assert "должна быть числом" in str(e)


def test_from_dict():
    """Тест создания вакансии из словаря"""
    data = {
        'name': 'Python Developer',
        'url': 'https://hh.ru/vacancy/12345',
        'salary_from': 100000,
        'salary_to': 150000,
        'salary_currency': 'RUR',
        'description': 'Опыт работы с Python',
        'employer': 'Test Company',
        'experience': 'От 1 года',
        'employment': 'Полная занятость'
    }

    vacancy = Vacancy.from_dict(data)
    assert vacancy.name == 'Python Developer'
    assert vacancy.url == 'https://hh.ru/vacancy/12345'
    assert vacancy.salary_from == 100000
    assert vacancy.employer == 'Test Company'


def test_to_dict():
    """Тест преобразования вакансии в словарь"""
    vacancy = Vacancy(
        name='Python Developer',
        url='https://hh.ru/vacancy/12345',
        salary_from=100000,
        salary_to=150000,
        salary_currency='RUR'
    )

    data = vacancy.to_dict()
    assert data['name'] == 'Python Developer'
    assert data['url'] == 'https://hh.ru/vacancy/12345'
    assert data['salary_from'] == 100000
    assert data['salary_to'] == 150000
    assert data['salary_currency'] == 'RUR'
