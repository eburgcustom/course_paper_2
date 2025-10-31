import os


from src.headhunter import HeadHunterAPI
from src.models import Vacancy
from src.storage import JSONStorage
from src.utils import (
    filter_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies,
    print_vacancies,
    save_vacancies_to_file
)


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем через консоль"""
    print("Добро пожаловать в программу поиска вакансий!")
    print("=" * 50)
    
    # Инициализация API и хранилища
    hh_api = HeadHunterAPI()
    storage = JSONStorage('vacancies.json')
    
    while True:
        print("\nМеню:")
        print("1. Поиск вакансий на hh.ru")
        print("2. Просмотр сохраненных вакансий")
        print("3. Фильтрация вакансий")
        print("4. Удаление вакансии")
        print("5. Сохранить текущие вакансии в файл")
        print("6. Выход")
        
        choice = input("\nВыберите действие (1-6): ").strip()
        
        if choice == '1':
            search_query = input("\nВведите поисковый запрос (например, 'Python разработчик'): ").strip()
            if not search_query:
                print("Ошибка: поисковый запрос не может быть пустым")
                continue
                
            try:
                per_page = int(input("Количество вакансий для загрузки (по умолчанию 50): ") or "50")
                only_with_salary = input("Только с указанием зарплаты? (да/нет): ").lower() == 'да'
                
                print("\nИдет загрузка вакансий...")
                vacancies = hh_api.get_vacancies(
                    search_query=search_query,
                    per_page=per_page,
                    only_with_salary=only_with_salary
                )
                
                if not vacancies:
                    print("По вашему запросу вакансии не найдены.")
                    continue
                
                # Сохраняем вакансии в хранилище
                for v in vacancies:
                    vacancy = Vacancy.from_dict(v)
                    try:
                        storage.add_vacancy(vacancy)
                    except ValueError as e:
                        # Пропускаем дубликаты
                        pass
                
                print(f"\nЗагружено {len(vacancies)} вакансий.")
                
                # Выводим топ-5 вакансий
                print("\nТоп-5 вакансий по зарплате:")
                sorted_vacancies = sort_vacancies(vacancies)
                top_vacancies = get_top_vacancies(sorted_vacancies, 5)
                print_vacancies(top_vacancies)
                
                # Предлагаем сохранить в файл
                if input("\nХотите сохранить результаты в файл? (да/нет): ").lower() == 'да':
                    filename = input("Введите имя файла (по умолчанию 'vacancies.json'): ") or 'vacancies.json'
                    save_vacancies_to_file(vacancies, filename)
                
            except ValueError as e:
                print(f"Ошибка: {e}")
            except Exception as e:
                print(f"Произошла ошибка: {e}")
        
        elif choice == '2':
            # Просмотр сохраненных вакансий
            vacancies = storage.get_vacancies()
            if not vacancies:
                print("\nСохраненных вакансий нет.")
                continue
                
            print(f"\nВсего сохранено вакансий: {len(vacancies)}")
            print_vacancies(vacancies)
        
        elif choice == '3':
            # Фильтрация вакансий
            vacancies = storage.get_vacancies()
            if not vacancies:
                print("\nНет вакансий для фильтрации.")
                continue
            
            # Фильтрация по ключевым словам
            filter_words = input("\nВведите ключевые слова для фильтрации (через пробел): ").strip().split()
            filtered = filter_vacancies(vacancies, filter_words)
            
            # Фильтрация по зарплате
            salary_range = input("Введите диапазон зарплат (например, 100000-200000): ").strip()
            if salary_range:
                filtered = get_vacancies_by_salary(filtered, salary_range)
            
            # Сортировка
            sorted_vacancies = sort_vacancies(filtered)
            
            # Вывод топ N
            try:
                top_n = int(input("Сколько вакансий показать? (по умолчанию все): ") or "0")
                result_vacancies = get_top_vacancies(sorted_vacancies, top_n) if top_n > 0 else sorted_vacancies
                print_vacancies(result_vacancies)
            except ValueError:
                print("Ошибка: введите корректное число")
        
        elif choice == '4':
            # Удаление вакансии
            vacancies = storage.get_vacancies()
            if not vacancies:
                print("\nНет вакансий для удаления.")
                continue
                
            print("\nСписок вакансий для удаления:")
            for i, v in enumerate(vacancies, 1):
                print(f"{i}. {v.get('name')} (ID: {v.get('id')})")
            
            try:
                vacancy_id = input("\nВведите ID вакансии для удаления: ").strip()
                if not vacancy_id:
                    print("Ошибка: ID не может быть пустым")
                    continue
                
                storage.delete_vacancy(vacancy_id)
                print(f"Вакансия с ID {vacancy_id} успешно удалена.")
            except ValueError as e:
                print(f"Ошибка: {e}")
            except Exception as e:
                print(f"Произошла ошибка: {e}")
        
        elif choice == '5':
            # Сохранение в файл
            vacancies = storage.get_vacancies()
            if not vacancies:
                print("\nНет вакансий для сохранения.")
                continue
                
            filename = input("\nВведите имя файла (по умолчанию 'vacancies_export.json'): ") or 'vacancies_export.json'
            save_vacancies_to_file(vacancies, filename)
        
        elif choice == '6':
            print("\nСпасибо за использование программы! До свидания!")
            break
        
        else:
            print("\nОшибка: неверный выбор. Пожалуйста, выберите действие от 1 до 6.")


if __name__ == "__main__":
    # Создаем директорию для данных, если её нет
    os.makedirs('data', exist_ok=True)
    
    try:
        user_interaction()
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем.")
    except Exception as e:
        print(f"\nПроизошла непредвиденная ошибка: {e}")
        raise