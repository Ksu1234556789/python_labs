"""
Модуль интерфейса командной строки.
Только ввод/вывод, никакой бизнес-логики.
"""
from typing import List, Optional
from app import CourseManager
from base import Course
from models import ProgrammingCourse, LanguageCourse, BusinessCourse
from exceptions import CourseNotFoundError, DuplicateCourseError, ValidationError
from strategies import (
    by_title, by_teacher, by_cost, by_hours, by_students_count,
    is_active, make_min_students_filter
)

class CLI:
    """Класс консольного интерфейса для управления курсами."""
    
    def __init__(self, manager: CourseManager) -> None:
        """
        Инициализация CLI.
        
        Args:
            manager: менеджер курсов
        """
        self.manager = manager
    

    def _format_title(self, title: str) -> str:
        """Каждое слово с большой буквы: 'python basics' → 'Python Basics'"""
        return ' '.join(word.capitalize() for word in title.split())
    
    def _format_name(self, name: str) -> str:
        """Каждое слово с большой буквы: 'иван иванов' → 'Иван Иванов'"""
        return ' '.join(word.capitalize() for word in name.split())
    
    # ... всё остальное без изменений

    def run(self) -> None:
        """Запускает главный цикл меню."""
        print("\n╔══════════════════════════════════════╗")
        print("║   Система управления курсами v1.0    ║")
        print("╚══════════════════════════════════════╝")
        
        while True:
            self._show_menu()
            choice = self._get_int_input("Выберите пункт меню: ")
            
            if choice == 0:
                self._confirm_exit()
                break
            elif choice == 1:
                self._add_course_menu()
            elif choice == 2:
                self._show_all_courses()
            elif choice == 3:
                self._search_course()
            elif choice == 4:
                self._filter_courses_menu()
            elif choice == 5:
                self._sort_courses_menu()
            elif choice == 6:
                self._remove_course_menu()
            elif choice == 7:
                self._save_data()
            else:
                print("❌ Ошибка: неверный пункт меню. Попробуйте снова.")
    
    # ============ Меню и ввод ============
    
    def _show_menu(self) -> None:
        """Отображает главное меню."""
        print("\n" + "=" * 40)
        print("│           ГЛАВНОЕ МЕНЮ               │")
        print("=" * 40)
        print("│ 1. Добавить курс                     │")
        print("│ 2. Показать все курсы                │")
        print("│ 3. Найти курс по названию            │")
        print("│ 4. Фильтровать курсы                 │")
        print("│ 5. Сортировать курсы                 │")
        print("│ 6. Удалить курс                      │")
        print("│ 7. Сохранить данные                  │")
        print("│ 0. Выход                             │")
        print("=" * 40)
    
    def _get_int_input(self, prompt: str) -> int:
        """
        Безопасный ввод целого числа.
        
        Args:
            prompt: текст приглашения
            
        Returns:
            введённое число
        """
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("❌ Ошибка: введите целое число")

    
    def _get_float_input(self, prompt: str) -> float:
        """
        Безопасный ввод числа с плавающей точкой.
        
        Args:
            prompt: текст приглашения
            
        Returns:
            введённое число
        """
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("❌ Ошибка: введите число")
    
    def _get_non_empty_input(self, prompt: str) -> str:
        """
        Ввод непустой строки.
        
        Args:
            prompt: текст приглашения
            
        Returns:
            введённая строка
        """
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("❌ Ошибка: поле не может быть пустым")
    
    def _confirm_action(self, message: str) -> bool:
        """
        Запрашивает подтверждение действия.
        
        Args:
            message: сообщение для подтверждения
            
        Returns:
            True если подтверждено, False если отменено
        """
        while True:
            answer = input(f"{message} (y/n): ").lower().strip()
            if answer in ['y', 'yes', 'да']:
                return True
            elif answer in ['n', 'no', 'нет']:
                return False
            print("❌ Введите y или n")
    
    # ============ Операции меню ============
    
    def _add_course_menu(self) -> None:
        """Меню добавления нового курса."""
        print("\n--- Добавление нового курса ---")
        print("Типы курсов:")
        print("  1. Курс программирования")
        print("  2. Языковой курс")
        print("  3. Бизнес-курс")
        
        course_type = self._get_int_input("Выберите тип курса (1-3): ")
        
        if course_type not in [1, 2, 3]:
            print("❌ Неверный тип курса")
            return
        
        try:
            title = self._format_title(self._get_non_empty_input("Название курса: "))
            teacher = self._format_name(self._get_non_empty_input("Преподаватель (Имя Фамилия): "))
            hours = self._get_int_input("Количество часов: ")
            students_count = self._get_int_input("Количество студентов: ")
            
            if course_type == 1:
                language = self._get_non_empty_input("Язык программирования: ")
                project_count = self._get_int_input("Количество проектов: ")
                course = self.manager.create_programming_course(
                    title, teacher, hours, students_count, language, project_count
                )
            elif course_type == 2:
                print("Допустимые языки: Английский, Немецкий, Французский, "
          "Испанский, Итальянский, Китайский, Японский, Корейский, "
          "Русский, Арабский, Португальский, Турецкий, Хинди")
                language = self._get_non_empty_input("Изучаемый язык: ")
                print("Доступные уровни: A1, A2, B1, B2, C1, C2")
                level = self._get_non_empty_input("Уровень: ").upper()
                course = self.manager.create_language_course(
                    title, teacher, hours, students_count, language, level
                )
            else:
                certificate_input = input("Выдаётся сертификат? (y/n): ").lower().strip()
                certificate = certificate_input in ['y', 'yes', 'да']
                company_partner = input("Компания-партнёр (Enter если нет): ").strip()
                course = self.manager.create_business_course(
                    title, teacher, hours, students_count, certificate, company_partner
                )
            
            print(f"✅ Курс '{course.title}' успешно добавлен!")
            
        except (DuplicateCourseError, ValidationError, ValueError, TypeError) as e:
            print(f"❌ Ошибка: {e}")
    
    def _show_all_courses(self) -> None:
        """Отображает все курсы в коллекции."""
        courses = self.manager.get_all_courses()
        
        if not courses:
            print("\n📭 Коллекция курсов пуста")
            return
        
        print(f"\n📚 Все курсы ({len(courses)}):")
        print("-" * 70)
        
        for i, course in enumerate(courses, 1):
            self._print_course(i, course)
    
    def _print_course(self, index: int, course: Course) -> None:
        """
        Форматированный вывод одного курса.
        
        Args:
            index: порядковый номер
            course: объект курса
        """
        type_icon = {
            ProgrammingCourse: "💻",
            LanguageCourse: "🌍",
            BusinessCourse: "💼"
        }.get(type(course), "📘")
        
        print(f"{type_icon} {index}. {course.title}")
        print(f"   Преподаватель: {course.teacher}")
        print(f"   Часы: {course.hours}")
        print(f"   Студентов: {course.students_count}/{course.MAX_STUDENTS}")
        print(f"   Статус: {'🟢 активен' if course.active else '🔴 закрыт'}")
        print(f"   Стоимость: {course.calculate():,.0f} руб.")
        
        # Дополнительная информация по типу курса
        if isinstance(course, ProgrammingCourse):
            print(f"   Язык: {course.language} | Проектов: {course.project_count}")
        elif isinstance(course, LanguageCourse):
            print(f"   Язык: {course.language} | Уровень: {course.level}")
        elif isinstance(course, BusinessCourse):
            cert = "✅ есть" if course.certificate else "❌ нет"
            print(f"   Сертификат: {cert}")
            if course.company_partner:
                print(f"   Партнёр: {course.company_partner}")
        
        print()
    
    def _search_course(self) -> None:
        """Поиск курсов по названию."""
        query = input("\n🔍 Введите название курса для поиска: ").strip()
        
        if not query:
            print("❌ Пустой запрос")
            return
        
        results = self.manager.search_by_title(query)
        
        if not results:
            print(f"❌ Курсы, содержащие '{query}' в названии, не найдены")
            return
        
        print(f"\n🔍 Найдено курсов: {len(results)}")
        print("-" * 70)
        for i, course in enumerate(results, 1):
            self._print_course(i, course)
    
    def _filter_courses_menu(self) -> None:
        """Меню фильтрации курсов."""
        print("\n--- Фильтрация курсов ---")
        print("1. По типу курса")
        print("2. По диапазону цен")
        print("3. Только активные")
        print("4. По количеству студентов (мин)")
        
        filter_type = self._get_int_input("Выберите фильтр (1-4): ")
        
        if filter_type == 1:
            print("\nТипы: programming, language, business")
            course_type = input("Введите тип курса: ").strip().lower()
            try:
                results = self.manager.filter_by_type(course_type)
            except ValidationError as e:
                print(f"❌ {e}")
                return
        elif filter_type == 2:
            min_price = self._get_float_input("Минимальная цена: ")
            max_price = self._get_float_input("Максимальная цена: ")
            results = self.manager.filter_by_price_range(min_price, max_price)
        elif filter_type == 3:
            results = self.manager.filter_active_courses()
        elif filter_type == 4:
            min_students = self._get_int_input("Минимальное количество студентов: ")
            results = self.manager.filter_courses(
                make_min_students_filter(min_students)
            )
        else:
            print("❌ Неверный фильтр")
            return
        
        self._display_filtered_results(results)
    
    def _display_filtered_results(self, courses: List[Course]) -> None:
        """Отображает результаты фильтрации."""
        if not courses:
            print("📭 Курсы не найдены по заданным критериям")
            return
        
        print(f"\n📊 Найдено курсов: {len(courses)}")
        print("-" * 70)
        for i, course in enumerate(courses, 1):
            self._print_course(i, course)
    
    def _sort_courses_menu(self) -> None:
        """Меню сортировки курсов."""
        print("\n--- Сортировка курсов ---")
        print("1. По названию")
        print("2. По преподавателю")
        print("3. По стоимости")
        print("4. По часам")
        print("5. По количеству студентов")
        
        sort_type = self._get_int_input("Выберите сортировку (1-5): ")
        
        if sort_type == 1:
            courses = self.manager.sort_by_title()
            print("\n📋 Сортировка по названию:")
        elif sort_type == 2:
            courses = self.manager.sort_by_teacher()
            print("\n📋 Сортировка по преподавателю:")
        elif sort_type == 3:
            courses = self.manager.sort_by_cost()
            print("\n📋 Сортировка по стоимости:")
        elif sort_type == 4:
            courses = self.manager.sort_by_hours()
            print("\n📋 Сортировка по часам:")
        elif sort_type == 5:
            courses = self.manager.sort_by_students()
            print("\n📋 Сортировка по количеству студентов:")
        else:
            print("❌ Неверная сортировка")
            return
        
        if not courses:
            print("📭 Коллекция пуста")
            return
        
        print("-" * 70)
        for i, course in enumerate(courses, 1):
            self._print_course(i, course)
    
    def _remove_course_menu(self) -> None:
        """Меню удаления курса с подтверждением."""
        print("\n--- Удаление курса ---")
        title = self._get_non_empty_input("Название курса: ")
        teacher = self._get_non_empty_input("Преподаватель: ")
        
        try:
            course = self.manager.find_course(title, teacher)
            if not course:
                raise CourseNotFoundError(f"{title} - {teacher}")
            
            # Показываем информацию о курсе перед удалением
            print("\nБудет удалён курс:")
            self._print_course(1, course)
            
            if self._confirm_action(f"Удалить '{title}' ({teacher})?"):
                self.manager.remove_course(title, teacher)
                print(f"✅ Курс '{title}' удалён")
            else:
                print("❎ Удаление отменено")
                
        except CourseNotFoundError as e:
            print(f"❌ {e}")
    
    def _save_data(self) -> None:
        """Сохраняет данные в файл."""
        try:
            self.manager.save_to_file()
            print("✅ Данные сохранены в courses_data.json")
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
    
    def _confirm_exit(self) -> None:
        """Подтверждение выхода с автосохранением."""
        if self._confirm_action("Сохранить данные перед выходом?"):
            self._save_data()
        print("\n👋 До свидания!")