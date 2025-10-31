from unittest.mock import MagicMock, patch

from src.headhunter import HeadHunterAPI


def test_get_vacancies_success():
    """Тест успешного получения вакансий"""
    # Создаем мок для requests.get
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'items': [
            {
                'name': 'Python Developer',
                'alternate_url': 'http://example.com/vacancy/1',
                'salary': {
                    'from': 100000,
                    'to': 150000,
                    'currency': 'RUR'
                },
                'snippet': {
                    'requirement': 'Опыт работы с Python',
                    'responsibility': 'Разработка приложений'
                },
                'employer': {
                    'name': 'Test Company'
                },
                'experience': {
                    'name': 'От 1 года до 3 лет'
                },
                'employment': {
                    'name': 'Полная занятость'
                }
            }
        ]
    }

    with patch('requests.get', return_value=mock_response):
        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Python")

        assert len(vacancies) == 1
        assert vacancies[0]['name'] == 'Python Developer'
        assert vacancies[0]['salary_from'] == 100000


def test_connect_failure():
    """Тест неудачного подключения"""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        try:
            HeadHunterAPI()
            assert False, "Должно быть вызвано исключение ConnectionError"
        except ConnectionError:
            pass  # Ожидаемое поведение
