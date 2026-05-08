"""
Демонстрация работы ЛР-5: функции как аргументы, стратегии, делегаты
"""
from base import Course
from models import ProgrammingCourse, LanguageCourse, BusinessCourse
from collection import OnlineSchool
import strategies as st


def print_section(title: str):
    """Вывод заголовка раздела"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_collection(collection, label: str = "Коллекция"):
    """Вывод коллекции с заголовком"""
    print(f"\n--- {label} ---")
    print(collection)


# ==================== СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ ====================

def create_test_collection() -> OnlineSchool:

    Course.existing_courses.clear()
    
    """Создание тестовой коллекции из 8 курсов"""
    school = OnlineSchool()
    
    # Программирование
    school.add(ProgrammingCourse("Python Pro", "Иванов А.А.", 40, 20, "Python", 5))
    school.add(ProgrammingCourse("Java Basics", "Петров Б.Б.", 30, 15, "Java", 3))
    school.add(ProgrammingCourse("Web Dev", "Сидоров В.В.", 50, 25, "JavaScript", 8))
    
    # Языки
    school.add(LanguageCourse("English A1", "Смирнова Г.Д.", 20, 12, "English", "A1"))
    school.add(LanguageCourse("Deutsch B1", "Мюллер Ф.Ф.", 25, 8, "German", "B1"))
    school.add(LanguageCourse("French A2", "Дюпон Ж.Ж.", 18, 22, "French", "A2"))
    
    # Бизнес
    school.add(BusinessCourse("MBA Start", "Козлов Д.Е.", 60, 10, True))
    school.add(BusinessCourse("Управление проектами", "Новикова Е.Ж.", 35, 18, False))
    
    # Закроем один курс для тестов
    school[2].close()  # Web Dev закрыт
    
    return school


# ==================== СЦЕНАРИЙ 1: Сортировка разными стратегиями ====================

def scenario_1_sorting():
    """Сценарий 1: Демонстрация сортировки коллекции разными стратегиями"""
    print_section("СЦЕНАРИЙ 1: СОРТИРОВКА РАЗНЫМИ СТРАТЕГИЯМИ")
    
    school = create_test_collection()
    print_collection(school, "Исходная коллекция")
    
    # 1. Сортировка по названию
    sorted_by_title = school.sort_by(st.by_title)
    print_collection(sorted_by_title, "Сортировка по названию (by_title)")
    
    # 2. Сортировка по стоимости
    sorted_by_cost = school.sort_by(st.by_cost)
    print_collection(sorted_by_cost, "Сортировка по стоимости (by_cost)")
    
    # 3. Сортировка по нескольким атрибутам (тип + стоимость)
    sorted_by_type_cost = school.sort_by(st.by_type_and_cost)
    print_collection(sorted_by_type_cost, "Сортировка по типу и стоимости (by_type_and_cost)")
    
    # 4. Сортировка по количеству студентов (lambda)
    sorted_by_students = school.sort_by(lambda c: c.students_count, reverse=True)
    print_collection(sorted_by_students, "Сортировка по студентам (lambda, убывание)")


# ==================== СЦЕНАРИЙ 2: Фильтрация ====================

def scenario_2_filtering():
    """Сценарий 2: Демонстрация фильтрации разными стратегиями"""
    print_section("СЦЕНАРИЙ 2: ФИЛЬТРАЦИЯ РАЗНЫМИ СТРАТЕГИЯМИ")
    
    school = create_test_collection()
    print_collection(school, "Исходная коллекция")
    
    # 1. Фильтрация: только дорогие курсы
    expensive = school.filter_by(st.is_expensive)
    print_collection(expensive, "Фильтр: дорогие курсы (> 5000 руб)")
    
    # 2. Фильтрация: только активные И популярные
    popular_active = school.filter_by(st.is_popular)
    print_collection(popular_active, "Фильтр: активные и популярные (> 20 студентов)")
    
    # 3. Фильтрация по типу (isinstance)
    programming_only = school.filter_by(st.is_programming)
    print_collection(programming_only, "Фильтр: только ProgrammingCourse (isinstance)")
    
    # 4. Фильтрация с использованием фабрики функций
    cheap_filter = st.make_price_filter(3000)
    cheap = school.filter_by(cheap_filter)
    print_collection(cheap, "Фильтр-фабрика: курсы <= 3000 руб")
    
    # 5. Сравнение lambda и именованной функции
    lambda_result = school.filter_by(lambda c: c.hours >= 30)
    named_result = school.filter_by(st.make_hours_range_filter(30, 100))
    print_collection(lambda_result, "Фильтр lambda: часы >= 30")
    print_collection(named_result, "То же самое через фабрику make_hours_range_filter(30, 100)")


# ==================== СЦЕНАРИЙ 3: map() и преобразования ====================

def scenario_3_map():
    """Сценарий 3: Демонстрация map() для преобразования коллекции"""
    print_section("СЦЕНАРИЙ 3: map() И ПРЕОБРАЗОВАНИЯ")
    
    school = create_test_collection()
    
    # 1. Извлечение названий через именованную функцию
    titles = school.map(st.extract_title)
    print("\nИзвлечение названий (map + extract_title):")
    for t in titles:
        print(f"  - {t}")
    
    # 2. Преобразование в словари
    dicts = school.map(st.to_dict)
    print("\nПреобразование в словари (map + to_dict):")
    for d in dicts:
        print(f"  {d}")
    
    # 3. Преобразование в строки-сводки через lambda
    summaries = school.map(lambda c: f"{c.title}: {c.calculate()} руб.")
    print("\nСтроки-сводки через lambda:")
    for s in summaries:
        print(f"  {s}")
    
    # 4. Применение скидки через lambda (расчёт)
    discounted_prices = school.map(lambda c: (c.title, round(c.calculate() * 0.9, 2)))
    print("\nЦены со скидкой 10% (lambda):")
    for title, price in discounted_prices:
        print(f"  {title}: {price} руб")


# ==================== СЦЕНАРИЙ 4: Callable-стратегии ====================

def scenario_4_callable():
    """Сценарий 4: Демонстрация callable-объектов как стратегий"""
    print_section("СЦЕНАРИЙ 4: CALLABLE-СТРАТЕГИИ")
    
    school = create_test_collection()
    
    # Стратегия 1: Скидка 15%
    discount_15 = st.DiscountStrategy(15)
    print("\nПрименение стратегии DiscountStrategy(15%):")
    results = school.map(discount_15)
    for r in results:
        print(f"  {r['title']}: {r['original_cost']} -> {r['new_cost']} руб (скидка {r['discount']})")
    
    # Стратегия 2: Скидка 25% (другая стратегия — тот же интерфейс)
    discount_25 = st.DiscountStrategy(25)
    print("\nПрименение стратегии DiscountStrategy(25%):")
    results = school.map(discount_25)
    for r in results:
        print(f"  {r['title']}: {r['original_cost']} -> {r['new_cost']} руб (скидка {r['discount']})")
    
    # Стратегия 3: LabelStrategy
    label_en = st.LabelStrategy("COURSE")
    print("\nПрименение LabelStrategy('COURSE'):")
    labels = school.map(label_en)
    for l in labels:
        print(f"  {l}")
    
    # Стратегия 4: LabelStrategy с другим префиксом
    label_ru = st.LabelStrategy("КУРС")
    print("\nПрименение LabelStrategy('КУРС') — та же стратегия, другой параметр:")
    labels = school.map(label_ru)
    for l in labels:
        print(f"  {l}")


# ==================== СЦЕНАРИЙ 5: Цепочка операций ====================

def scenario_5_chain():
    """Сценарий 5: Цепочка операций filter -> sort -> apply"""
    print_section("СЦЕНАРИЙ 5: ЦЕПОЧКА ОПЕРАЦИЙ")
    
    school = create_test_collection()
    print_collection(school, "Исходная коллекция")
    
    # Шаг 1: Фильтрация — только активные курсы
    filtered = school.filter_by(st.is_active)
    print_collection(filtered, "Шаг 1: filter_by(is_active)")
    
    # Шаг 2: Сортировка — по стоимости
    sorted_collection = filtered.sort_by(st.by_cost)
    print_collection(sorted_collection, "Шаг 2: sort_by(by_cost)")
    
    # Шаг 3: Применение — добавляем студентов через UpgradeStrategy
    upgrade = st.UpgradeStrategy(students_to_add=3)
    result = sorted_collection.apply(upgrade)
    print_collection(result, "Шаг 3: apply(UpgradeStrategy(3)) — добавлено по 3 студента")
    
    # Цепочка в одну строку (альтернативный синтаксис)
    print("\n--- Цепочка в одну строку ---")
    chain_result = (school
        .filter_by(st.is_active)
        .sort_by(st.by_cost)
        .apply(st.UpgradeStrategy(2)))
    print_collection(chain_result, "filter_by(is_active) -> sort_by(by_cost) -> apply(UpgradeStrategy(2))")
    
    # Демонстрация заменяемости стратегий
    print("\n--- Замена стратегии без изменения кода ---")
    chain_result_2 = (school
        .filter_by(st.is_programming)  # другой фильтр
        .sort_by(st.by_students_count)  # другая сортировка
        .apply(st.UpgradeStrategy(5)))  # другой параметр
    print_collection(chain_result_2, "filter_by(is_programming) -> sort_by(by_students_count) -> apply(UpgradeStrategy(5))")


# ==================== СЦЕНАРИЙ 6: Демонстрация методов sort_by/filter_by коллекции ====================

def scenario_6_methods():
    """Сценарий 6: Использование методов sort_by() и filter_by() коллекции"""
    print_section("СЦЕНАРИЙ 6: МЕТОДЫ sort_by() И filter_by() КОЛЛЕКЦИИ")
    
    school = create_test_collection()
    
    # filter_by с лямбдой
    cheap_and_active = school.filter_by(lambda c: c.calculate() < 5000 and c.active)
    print_collection(cheap_and_active, "filter_by(lambda c: стоимость < 5000 И активен)")
    
    # sort_by с сортировкой по нескольким полям через lambda
    sorted_complex = school.sort_by(lambda c: (c.students_count, -c.hours))
    print_collection(sorted_complex, "sort_by(lambda: студенты по возр., часы по убыв.)")
    
    # Сравнение lambda и именованной функции
    print("\n--- Сравнение lambda и именованной функции ---")
    by_title_lambda = school.sort_by(lambda c: c.title.lower())
    by_title_named = school.sort_by(st.by_title)
    print("Результат lambda и именованной функции by_title идентичен:", 
          [c.title for c in by_title_lambda] == [c.title for c in by_title_named])


# ==================== ЗАПУСК ВСЕХ СЦЕНАРИЕВ ====================

if __name__ == "__main__":
    print("=" * 70)
    print("  ЛАБОРАТОРНАЯ РАБОТА №5: ФУНКЦИИ КАК АРГУМЕНТЫ. СТРАТЕГИИ И ДЕЛЕГАТЫ")
    print("=" * 70)
    
    scenario_1_sorting()
    scenario_2_filtering()
    scenario_3_map()
    scenario_4_callable()
    scenario_5_chain()
    scenario_6_methods()
    
    print("\n" + "=" * 70)
    print("  ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 70)