from typing import Any, Dict, Optional


class Vacancy:
    """Класс для представления вакансии"""

    def __init__(
        self,
        name: str,
        url: str,
        salary_from: Optional[int] = None,
        salary_to: Optional[int] = None,
        salary_currency: Optional[str] = None,
        description: str = "",
        employer: Optional[str] = None,
        experience: Optional[str] = None,
        employment: Optional[str] = None
    ):
        self.name = name
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency
        self.description = description
        self.employer = employer
        self.experience = experience
        self.employment = employment

        # Валидация данных при инициализации
        self._validate_salary()
        self._validate_url()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return False
        return self.name == other.name and self.url == other.url

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return (self.name, self.url) < (other.name, other.url)

    def __hash__(self) -> int:
        return hash((self.name, self.url))

    def _validate_salary(self) -> None:
        """Проверка корректности данных о зарплате"""
        if self.salary_from is not None and not isinstance(self.salary_from, (int, float)):
            raise ValueError("Зарплата 'от' должна быть числом")
        if self.salary_to is not None and not isinstance(self.salary_to, (int, float)):
            raise ValueError("Зарплата 'до' должна быть числом")

    def _validate_url(self) -> None:
        """Проверка корректности URL"""
        if not isinstance(self.url, str) or not self.url.startswith(('http://', 'https://')):
            raise ValueError("Некорректный URL вакансии")

    @property
    def salary(self) -> str:
        """Возвращает отформатированную строку с зарплатой"""
        if self.salary_from is not None and self.salary_to is not None:
            return f"{self.salary_from:,} - {self.salary_to:,} {self.salary_currency or ''}".replace(',', ' ')
        elif self.salary_from is not None:
            return f"от {self.salary_from:,} {self.salary_currency or ''}".replace(',', ' ')
        elif self.salary_to is not None:
            return f"до {self.salary_to:,} {self.salary_currency or ''}".replace(',', ' ')
        return "Зарплата не указана"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Vacancy':
        """Создает экземпляр Vacancy из словаря"""
        return cls(
            name=data.get('name', ''),
            url=data.get('url', ''),
            salary_from=data.get('salary_from'),
            salary_to=data.get('salary_to'),
            salary_currency=data.get('salary_currency'),
            description=data.get('description', ''),
            employer=data.get('employer'),
            experience=data.get('experience'),
            employment=data.get('employment')
        )

    def to_dict(self) -> Dict[str, Any]:
        """Возвращает словарь с данными вакансии"""
        return {
            'name': self.name,
            'url': self.url,
            'salary_from': self.salary_from,
            'salary_to': self.salary_to,
            'salary_currency': self.salary_currency,
            'description': self.description,
            'employer': self.employer,
            'experience': self.experience,
            'employment': self.employment
        }

    def __str__(self) -> str:
        """Строковое представление вакансии"""
        return (
            f"{self.name}\n"
            f"Зарплата: {self.salary}\n"
            f"Компания: {self.employer or 'Не указано'}\n"
            f"Требования: {self.description or 'Не указаны'}\n"
            f"Опыт: {self.experience or 'Не указан'}\n"
            f"Тип занятости: {self.employment or 'Не указан'}\n"
            f"Ссылка: {self.url}\n"
            "-" * 50
        )
