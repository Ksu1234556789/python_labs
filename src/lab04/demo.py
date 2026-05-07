from models import ProgrammingCourse, LanguageCourse, BusinessCourse
from collection import OnlineSchool
from interfaces import Printable, Comparable


def print_all(items: list[Printable]):
    for item in items:
        print(item.to_string())


def compare_all(items: list[Comparable]):
    for i in range(len(items) - 1):
        a = items[i]
        b = items[i + 1]
        print(f"{a.title} vs {b.title}: {a.compare_to(b)}")


def main():
    school = OnlineSchool()

    c1 = ProgrammingCourse("Python", "Иванов", 40, 10, "Python", 3)
    c2 = LanguageCourse("English", "Smith", 30, 8, "English", "B1")
    c3 = BusinessCourse("Marketing", "Петров", 25, 12, True)

    school.add(c1)
    school.add(c2)
    school.add(c3)

    print("=== 1. Printable ===")
    print_all(school.get_printable())

    print("\n=== 2. Comparable ===")
    compare_all(school.get_comparable())

    print("\n=== 3. Полиморфизм ===")
    for c in school:
        print(c.process())

    print("\n=== 4. isinstance ===")
    for c in school:
        print(c.title,
              isinstance(c, Printable),
              isinstance(c, Comparable))

    print("\n=== 5. Сортировка ===")
    for c in school.sort_by_comparable():
        print(c.to_string())

    print("\n=== 6. Collection print_all ===")
    school.print_all()


if __name__ == "__main__":
    main()