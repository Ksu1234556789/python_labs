from models import OnlineCourse, OfflineCourse
from collection import OnlineSchool


def main():
    print("\n=== ЛР3: Наследование и полиморфизм ===")

    # ===== СОЗДАНИЕ ОБЪЕКТОВ =====
    c1 = OnlineCourse("Python", "Иванов", 40, 20, "Stepik", 100)
    c2 = OfflineCourse("Java", "Петров", 50, 15, "Москва", "101")
    c3 = OnlineCourse("C++", "Сидоров", 60, 10, "Coursera", 120)

    # ===== ЕДИНАЯ КОЛЛЕКЦИЯ =====
    school = OnlineSchool()
    for c in [c1, c2, c3]:
        school.add(c)

    print("\n--- Все курсы ---")
    for c in school:
        print(c)

    # ===== ПОЛИМОРФИЗМ (без if!) =====
    print("\n--- Полиморфизм calculate() ---")
    for c in school:
        print(f"{c.title}: результат = {c.calculate()}")

    # ===== isinstance =====
    print("\n--- Проверка типов ---")
    for c in school:
        if isinstance(c, OnlineCourse):
            print(f"{c.title} — онлайн курс")
        elif isinstance(c, OfflineCourse):
            print(f"{c.title} — офлайн курс")

    # ===== ФИЛЬТРАЦИЯ ПО ТИПУ =====
    print("\n--- Только онлайн курсы ---")
    online_courses = [c for c in school if isinstance(c, OnlineCourse)]
    for c in online_courses:
        print(c)

    # ===== СЦЕНАРИЙ 1 =====
    print("\n--- СЦЕНАРИЙ 1: расчёт прибыли ---")
    total = sum(c.calculate() for c in school)
    print("Общий результат:", total)

    # ===== СЦЕНАРИЙ 2 =====
    print("\n--- СЦЕНАРИЙ 2: работа методов ---")
    print(c1.connect())
    print(c2.attend())

    # ===== СЦЕНАРИЙ 3 =====
    print("\n--- СЦЕНАРИЙ 3: активные курсы ---")
    c2.close()
    active = school.get_active_courses()
    for c in active:
        print(c)


if __name__ == "__main__":
    main()