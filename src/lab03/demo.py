"""
Демонстрация работы ЛР-3 (наследование, полиморфизм, интеграция с коллекцией)
"""

from models import ProgrammingCourse, LanguageCourse, BusinessCourse
from collection import OnlineSchool
from base import Course


def print_section(title):
    """Вывод заголовка секции"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_subsection(title):
    """Вывод подзаголовка"""
    print(f"\n--- {title} ---")


def create_school_with_courses():
    """Создание коллекции OnlineSchool с разными типами курсов"""
    # Очищаем множество существующих курсов перед созданием
    Course.existing_courses.clear()
    
    school = OnlineSchool()
    
    # Курсы программирования
    school.add(ProgrammingCourse(
        "Python Advanced", "Иванов И.И.", 40, 15,
        language="Python", project_count=5
    ))
    school.add(ProgrammingCourse(
        "Java Basics", "Сидоров С.С.", 32, 22,
        language="Java", project_count=3
    ))
    school.add(ProgrammingCourse(
        "JavaScript FullStack", "Петрова А.В.", 48, 12,
        language="JavaScript", project_count=7
    ))
    
    # Языковые курсы
    lang1 = LanguageCourse(
        "Английский для IT", "Smith J.", 60, 12,
        language="English", level="B1"
    )
    lang1.set_native_speaker(True)
    school.add(lang1)
    
    lang2 = LanguageCourse(
        "Немецкий с нуля", "Schmidt A.", 48, 8,
        language="German", level="A1"
    )
    school.add(lang2)
    
    lang3 = LanguageCourse(
        "Испанский интенсив", "Garcia M.", 36, 10,
        language="Spanish", level="A2"
    )
    school.add(lang3)
    
    # Бизнес-курсы
    school.add(BusinessCourse(
        "Управление проектами", "Петров П.П.", 32, 20,
        certificate=True, company_partner="IT Company"
    ))
    school.add(BusinessCourse(
        "Agile и Scrum", "Козлов К.К.", 24, 18,
        certificate=True, company_partner=""
    ))
    school.add(BusinessCourse(
        "Лидерство и команда", "Морозова М.М.", 28, 14,
        certificate=False, company_partner="HR Academy"
    ))
    school.add(BusinessCourse(
        "Бизнес-аналитика", "Волков В.В.", 36, 16,
        certificate=True, company_partner="Analytics Pro"
    ))
    
    return school


def demo_scenario_1(school):
    """Сценарий 1: Полиморфизм - вызов общего метода для всех объектов в коллекции"""
    print_section("СЦЕНАРИЙ 1: Полиморфизм без условий (process и calculate)")
    
    print(f"\nКоллекция содержит {len(school)} курсов разных типов:\n")
    
    # Правильный подход (полиморфизм):
    print("Вызов obj.process() для всех курсов:")
    print("-" * 70)
    for i, course in enumerate(school):
        print(f"{i+1}. {course.process()}")
    
    print("\n" + "-" * 70)
    print("\nВызов obj.calculate() для всех курсов:")
    print("-" * 70)
    print(f"{'№':<3} {'Тип курса':<20} {'Название':<25} {'Стоимость':<12}")
    print("-" * 70)
    
    total_cost = 0
    for i, course in enumerate(school):
        cost = course.calculate()
        total_cost += cost
        course_type = type(course).__name__
        print(f"{i+1:<3} {course_type:<20} {course.title:<25} {cost:>10.2f} р.")
    
    print("-" * 70)
    print(f"{'ИТОГО':<51} {total_cost:>10.2f} р.")


def demo_scenario_2(school):
    """Сценарий 2: Фильтрация по типу с использованием методов коллекции"""
    print_section("СЦЕНАРИЙ 2: Фильтрация по типу (использование методов OnlineSchool)")
    
    # Использование встроенных методов коллекции
    print_subsection("Курсы программирования (через school.get_programming_courses())")
    prog_courses = school.get_programming_courses()
    for i, c in enumerate(prog_courses, 1):
        print(f"  {i}. {c.title} — {c.language}, проектов: {c.project_count}")
        print(f"     Стоимость: {c.calculate():.2f} р., студентов: {c.students_count}")
    
    print_subsection("Языковые курсы (через school.get_language_courses())")
    lang_courses = school.get_language_courses()
    for i, c in enumerate(lang_courses, 1):
        native_str = " (носитель)" if c.native_speaker else ""
        print(f"  {i}. {c.title} — {c.language}, уровень: {c.level}{native_str}")
        print(f"     Стоимость: {c.calculate():.2f} р.")
        # Использование уникального метода
        if c.level in ['A1', 'A2']:
            print(f"     → {c.upgrade_level()}")
    
    print_subsection("Бизнес-курсы (через school.get_business_courses())")
    business_courses = school.get_business_courses()
    for i, c in enumerate(business_courses, 1):
        cert_str = "с сертификатом" if c.certificate else "без сертификата"
        partner_str = f", партнёр: {c.company_partner}" if c.has_partner() else ""
        print(f"  {i}. {c.title} — {cert_str}{partner_str}")
        print(f"     Стоимость: {c.calculate():.2f} р.")
    
    # Демонстрация уникальных методов каждой группы
    print_subsection("Уникальные методы групп")
    
    if prog_courses:
        c = prog_courses[0]
        print(f"Программирование: {c.add_project()}")
    
    if lang_courses:
        c = lang_courses[1]  # второй курс
        print(f"Языковой: {c.set_native_speaker(True)}")
    
    if business_courses:
        c = business_courses[-1]  # последний курс
        if not c.certificate:
            print(f"Бизнес: {c.issue_certificate()}")


def demo_scenario_3(school):
    """Сценарий 3: Интеграция с коллекцией и расширенная статистика"""
    print_section("СЦЕНАРИЙ 3: Расширенные методы коллекции и статистика")
    
    # 1. Сортировка по стоимости (используем метод коллекции)
    print_subsection("Сортировка по стоимости (все курсы)")
    school_copy = OnlineSchool()
    for c in school:
        school_copy.add(c)
    school_copy.sort_by_cost(reverse=True)
    
    print(f"{'№':<3} {'Тип':<20} {'Название':<25} {'Стоимость':<12}")
    print("-" * 70)
    
    # Вместо среза используем счётчик для вывода топ-5
    count = 0
    for course in school_copy:
        if count >= 5:  # Топ-5
            break
        count += 1
        print(f"{count:<3} {type(course).__name__:<20} {course.title:<25} {course.calculate():>10.2f} р.")
    
    # 2. Статистика по типам (новый метод коллекции)
    print_subsection("Статистика по типам курсов")
    stats = school.get_statistics_by_type()
    
    for course_type, data in stats.items():
        print(f"\n{course_type}:")
        print(f"  • Количество курсов: {data['count']}")
        print(f"  • Средняя стоимость: {data['avg_cost']:.2f} р.")
        print(f"  • Среднее количество студентов: {data['avg_students']:.1f}")
    
    # 3. Фильтрация в новую коллекцию (метод filter_by_type)
    print_subsection("Создание отдельных коллекций по типам")
    
    from models import ProgrammingCourse, BusinessCourse, LanguageCourse
    
    prog_collection = school.filter_by_type(ProgrammingCourse)
    print(f"Коллекция курсов программирования: {len(prog_collection)} курсов")
    
    lang_collection = school.filter_by_type(LanguageCourse)
    print(f"Коллекция языковых курсов: {len(lang_collection)} курса")
    
    biz_collection = school.filter_by_type(BusinessCourse)
    print(f"Коллекция бизнес-курсов: {len(biz_collection)} курса")
    
    # 4. Комбинированная фильтрация
    print_subsection("Комбинированная фильтрация")
    
    # Активные бизнес-курсы с сертификатом
    active_biz_with_cert = [
        c for c in school.get_business_courses()
        if c.active and c.certificate
    ]
    print(f"Активные бизнес-курсы с сертификатом: {len(active_biz_with_cert)}")
    for c in active_biz_with_cert:
        print(f"  • {c.title} — {c.calculate():.2f} р.")
    
    # Языковые курсы с уровнем B1 и выше
    high_level_lang = [
        c for c in school.get_language_courses()
        if c.level in ['B1', 'B2', 'C1', 'C2']
    ]
    print(f"\nЯзыковые курсы уровня B1 и выше: {len(high_level_lang)}")
    for c in high_level_lang:
        print(f"  • {c.title} — {c.language}, уровень: {c.level}")
    
    # Курсы программирования с большим количеством проектов
    complex_prog = [
        c for c in school.get_programming_courses()
        if c.project_count >= 5
    ]
    print(f"\nКурсы программирования с 5+ проектами: {len(complex_prog)}")
    for c in complex_prog:
        print(f"  • {c.title} — {c.language}, проектов: {c.project_count}")


def demo_scenario_4(school):
    """Сценарий 4: Проверка isinstance и полиморфное поведение"""
    print_section("СЦЕНАРИЙ 4: Проверка типов и полиморфное поведение")
    
    print("Демонстрация isinstance() для проверки типов:\n")
    
    type_counts = {
        "ProgrammingCourse": 0,
        "LanguageCourse": 0,
        "BusinessCourse": 0
    }
    
    for course in school:
        if isinstance(course, BusinessCourse):
            type_counts["BusinessCourse"] += 1
        elif isinstance(course, LanguageCourse):
            type_counts["LanguageCourse"] += 1
        elif isinstance(course, ProgrammingCourse):
            type_counts["ProgrammingCourse"] += 1
    
    for type_name, count in type_counts.items():
        if count > 0:
            print(f"  {type_name}: {count} курсов")
    
    print_subsection("Полиморфизм в действии: один вызов - разный результат")
    
    # Выбираем по одному объекту каждого типа
    prog = next((c for c in school if isinstance(c, ProgrammingCourse)), None)
    lang = next((c for c in school if isinstance(c, LanguageCourse)), None)
    biz = next((c for c in school if isinstance(c, BusinessCourse)), None)
    
    test_objects = [obj for obj in [prog, lang, biz] if obj is not None]
    
    print("\nВызов метода process():")
    print("-" * 70)
    for obj in test_objects:
        print(f"  {type(obj).__name__:20} → {obj.process()}")
    
    print("\nВызов метода calculate():")
    print("-" * 70)
    for obj in test_objects:
        print(f"  {type(obj).__name__:20} → {obj.calculate():.2f} р.")
    
    print("\nВызов метода __str__():")
    print("-" * 70)
    for obj in test_objects:
        print(f"  {obj}")


def main():
    """Главная функция демонстрации"""
    
    print("\n" + "=" * 70)
    print(" " * 15 + "ЛАБОРАТОРНАЯ РАБОТА №3")
    print(" " * 10 + "Наследование и иерархия классов")
    print("=" * 70)
    
    # Создаём коллекцию ОДИН раз
    school = create_school_with_courses()
    
    # Запускаем все сценарии
    demo_scenario_1(school)
    demo_scenario_2(school)
    demo_scenario_3(school)
    demo_scenario_4(school)
    
    print_section("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("  1. Иерархия классов (1 базовый + 3 дочерних)")
    print("  2. Абстрактные методы в базовом классе (process, calculate)")
    print("  3. Полиморфизм через process() и calculate()")
    print("  4. Интеграция с коллекцией OnlineSchool")
    print("  5. Методы фильтрации в коллекции (get_by_type, filter_by_type)")
    print("  6. Единый интерфейс без if type == ...")
    print("  7. Минимум 3 сценария (реализовано 4)")
    print("  8. Статистика и комбинированная фильтрация")


if __name__ == "__main__":
    main()