"""
ЛР-6 — Демонстрация TypedCollection и Protocol
"""

from container import (
    TypedCollection,
    DisplayableCollection,
    ScorableCollection,
    D,
    S,
    Displayable,
    Scorable,
    Student,
    Exam
)

from models import (
    ProgrammingCourse,
    LanguageCourse,
    BusinessCourse
)


# ==================== ВСПОМОГАТЕЛЬНОЕ ====================

def print_section(title: str) -> None:
    """Печать заголовка"""

    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


# ==================== MONKEY PATCHING ====================

def course_display(self) -> str:
    return (
        f"{self.title} | "
        f"Студентов: {self.students_count} | "
        f"Стоимость: {self.calculate():.2f}₽"
    )


def course_score(self) -> float:
    return round(
        (
            self.students_count / self.MAX_STUDENTS
        ) * 100,
        1
    )


# Добавляем методы динамически
ProgrammingCourse.display = course_display
ProgrammingCourse.score = course_score

LanguageCourse.display = course_display
LanguageCourse.score = course_score

BusinessCourse.display = course_display
BusinessCourse.score = course_score


# ==================== ЗАДАНИЕ НА 3 ====================

def demo_level_3() -> None:
    """
    Демонстрация Generic-коллекции
    """

    print_section(
        "Generic TypedCollection"
    )

    courses: TypedCollection[
        ProgrammingCourse
    ] = TypedCollection()

    py = ProgrammingCourse(
        "Python Pro",
        "Иванов",
        40,
        15,
        "Python",
        5
    )

    js = ProgrammingCourse(
        "JavaScript Fullstack",
        "Петров",
        50,
        20,
        "JavaScript",
        4
    )

    courses.add(py)
    courses.add(js)

    print(courses)

    print("\nВсе элементы:")

    for course in courses.get_all():
        print(
            f"  • {course.title} "
            f"({course.language})"
        )

    print(
        "\n✅ Типизация работает "
        "(mypy/pyright найдут ошибки)"
    )


# ==================== ЗАДАНИЕ НА 4 ====================

def demo_level_4() -> None:
    """
    Демонстрация find/filter/map
    """

    print_section(
        "find/filter/map"
    )

    all_courses: TypedCollection[
        ProgrammingCourse
        | LanguageCourse
        | BusinessCourse
    ] = TypedCollection()

    all_courses.add(
        ProgrammingCourse(
            "Python Pro",
            "Иванов",
            40,
            25,
            "Python",
            5
        )
    )

    all_courses.add(
        ProgrammingCourse(
            "Java Base",
            "Петров",
            30,
            10,
            "Java",
            3
        )
    )

    all_courses.add(
        LanguageCourse(
            "English A1",
            "Сидорова",
            20,
            30,
            "English",
            "A1"
        )
    )

    all_courses.add(
        BusinessCourse(
            "MBA Start",
            "Козлов",
            60,
            15,
            True
        )
    )

    # ===== find =====

    print("\n▶ find()")

    found = all_courses.find(
        lambda c: c.students_count > 20
    )

    print(f"Найден: {found}")

    not_found = all_courses.find(
        lambda c: c.students_count > 100
    )

    print(f"Не найден: {not_found}")

    # ===== filter =====

    print("\n▶ filter()")

    expensive = all_courses.filter(
        lambda c: c.calculate() > 5000
    )

    for item in expensive:
        print(
            f"  • {item.title}: "
            f"{item.calculate():.2f}₽"
        )

    # ===== map =====

    print("\n▶ map() -> list[str]")

    titles: list[str] = all_courses.map(
        lambda c: c.title
    )

    print(titles)

    print("\n▶ map() -> list[float]")

    prices: list[float] = all_courses.map(
        lambda c: c.calculate()
    )

    print(prices)

    print(
        "\n✅ map() меняет тип результата "
        "через TypeVar R"
    )


# ==================== ЗАДАНИЕ НА 5 ====================

def demo_level_5() -> None:
    """
    Демонстрация Protocol
    """

    print_section(
        "Protocol"
    )

    # ===== Проверка Protocol =====

    py = ProgrammingCourse(
        "Test",
        "Преподаватель",
        30,
        10,
        "Python",
        3
    )

    print("\n▶ isinstance() с Protocol")

    print(
        f"Displayable: "
        f"{isinstance(py, Displayable)}"
    )

    print(
        f"Scorable: "
        f"{isinstance(py, Scorable)}"
    )

    # ===== Сценарий 1 =====

    print_section(
        "СЦЕНАРИЙ 1 — DisplayableCollection"
    )

    displayable_collection: DisplayableCollection[D] = (
        DisplayableCollection()
    )

    displayable_collection.add(
        ProgrammingCourse(
            "Python Pro",
            "Иванов",
            40,
            25,
            "Python",
            5
        )
    )

    displayable_collection.add(
        LanguageCourse(
            "English A1",
            "Сидорова",
            20,
            30,
            "English",
            "A1"
        )
    )

    displayable_collection.add(
        BusinessCourse(
            "MBA Start",
            "Козлов",
            60,
            15,
            True
        )
    )

    displayable_collection.add(
        Student(
            "Анна Смирнова",
            4.8
        )
    )

    print("\nВсе display():")

    displayable_collection.display_all()

    print(
        "\n✅ Разные классы "
        "работают через Protocol"
    )

    # map()

    displays: list[str] = (
        displayable_collection.map(
            lambda item: item.display()
        )
    )

    print("\nmap(display):")

    for d in displays:
        print(f"  • {d}")

    # ===== Сценарий 2 =====

    print_section(
        "СЦЕНАРИЙ 2 — ScorableCollection"
    )

    scorable_collection: ScorableCollection[S] = (
        ScorableCollection()
    )

    scorable_collection.add(
        ProgrammingCourse(
            "Java Pro",
            "Петров",
            45,
            28,
            "Java",
            5
        )
    )

    scorable_collection.add(
        LanguageCourse(
            "Deutsch B2",
            "Фёдорова",
            25,
            8,
            "German",
            "B2"
        )
    )

    scorable_collection.add(
        BusinessCourse(
            "Бизнес-аналитика",
            "Новикова",
            35,
            5,
            False
        )
    )

    scorable_collection.add(
        Exam(
            "Математика",
            85.5
        )
    )

    print("\nВсе score():")

    for item in scorable_collection:
        print(
            f"  • {item} -> "
            f"{item.score()}"
        )

    scores = scorable_collection.get_scores()

    print(f"\nScores: {scores}")

    avg = scorable_collection.get_average_score()

    print(f"Average: {avg:.1f}")

    print(
        "\n✅ Один TypedCollection "
        "работает с разными Protocol"
    )

    # ===== Один класс = два Protocol =====

    print(
        "\n▶ ProgrammingCourse "
        "подходит под оба Protocol"
    )

    pc = ProgrammingCourse(
        "Fullstack",
        "Иванов",
        50,
        20,
        "JavaScript",
        4
    )

    print(pc.display())
    print(pc.score())


# ==================== ЗАПУСК ====================

if __name__ == "__main__":

    print("=" * 60)
    print("  ЛР-6 — GENERICS И TYPING")
    print("=" * 60)

    demo_level_3()
    demo_level_4()
    demo_level_5()

