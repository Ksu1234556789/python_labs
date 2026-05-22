
from typing import Callable, Any, List
from base import Course
from models import ProgrammingCourse, LanguageCourse, BusinessCourse


# ==================== СТРАТЕГИИ СОРТИРОВКИ ====================

def by_title(course: Course) -> str:
    """Стратегия сортировки по названию курса (в алфавитном порядке)"""
    return course.title.lower()


def by_teacher(course: Course) -> str:
    """Стратегия сортировки по имени преподавателя (в алфавитном порядке)"""
    return course.teacher.lower()


def by_cost(course: Course) -> float:
    """Стратегия сортировки по стоимости курса (по возрастанию)"""
    return course.calculate()


def by_hours(course: Course) -> int:
    """Стратегия сортировки по количеству часов (по возрастанию)"""
    return course.hours


def by_students_count(course: Course) -> int:
    """Стратегия сортировки по количеству студентов (по возрастанию)"""
    return course.students_count


def by_title_and_teacher(course: Course) -> tuple:
    """
    Стратегия сортировки по названию, затем по преподавателю
    
    Returns:
        Кортеж (название, преподаватель) для сортировки по двум атрибутам
    """
    return (course.title.lower(), course.teacher.lower())


def by_type_and_cost(course: Course) -> tuple:
    """
    Стратегия сортировки по типу курса, затем по стоимости
    
    Returns:
        Кортеж (название типа, стоимость)
    """
    type_order = {
        ProgrammingCourse: 0,
        LanguageCourse: 1,
        BusinessCourse: 2
    }
    course_type = type(type(course))
    type_index = type_order.get(course_type, 99)
    return (type_index, course.calculate())


# ==================== СТРАТЕГИИ ФИЛЬТРАЦИИ ====================

def is_active(course: Course) -> bool:
    """Фильтр: курс активен"""
    return course.active


def is_expensive(course: Course) -> bool:
    """Фильтр: дорогой курс (стоимость > 5000)"""
    return course.calculate() > 5000


def is_cheap(course: Course) -> bool:
    """Фильтр: дешёвый курс (стоимость <= 3000)"""
    return course.calculate() <= 3000


def has_many_students(course: Course) -> bool:
    """Фильтр: курс с большим количеством студентов (> 15)"""
    return course.students_count > 15


def is_popular(course: Course) -> bool:
    """Фильтр: популярный курс (> 20 студентов И активный)"""
    return course.active and course.students_count > 20


def is_programming(course: Course) -> bool:
    """Фильтр: курс программирования (по типу объекта)"""
    return isinstance(course, ProgrammingCourse)


def is_language(course: Course) -> bool:
    """Фильтр: языковой курс (по типу объекта)"""
    return isinstance(course, LanguageCourse)


# ==================== ФУНКЦИИ-ОБРАБОТЧИКИ (для map и apply) ====================

def to_dict(course: Course) -> dict:
    """
    Преобразование курса в словарь с основными данными
    
    Returns:
        Словарь с ключами: title, teacher, hours, students, cost, type, active
    """
    return {
        'title': course.title,
        'teacher': course.teacher,
        'hours': course.hours,
        'students': course.students_count,
        'cost': course.calculate(),
        'type': type(course).__name__,
        'active': course.active
    }


def to_summary(course: Course) -> str:
    """
    Преобразование курса в краткую строку-сводку
    
    Returns:
        Строка вида "Python Basics (ProgrammingCourse): 6500.0 руб, 20 студентов"
    """
    return f"{course.title} ({type(course).__name__}): {course.calculate()} руб, {course.students_count} студентов"


def extract_title(course: Course) -> str:
    """Извлечение названия курса"""
    return course.title


def extract_cost(course: Course) -> float:
    """Извлечение стоимости курса"""
    return course.calculate()


def add_student_to_course(course: Course) -> Course:
    """
    Добавление одного студента на курс (если возможно)
    Возвращает тот же объект курса
    """
    try:
        course.add_student()
    except (ValueError, RuntimeError):
        pass  # курс заполнен или закрыт
    return course


# ==================== ФАБРИКИ ФУНКЦИЙ ====================

def make_price_filter(max_price: float) -> Callable[[Course], bool]:
    """
    Фабрика функций: создаёт фильтр по максимальной цене
    
    Args:
        max_price: максимальная стоимость курса
    
    Returns:
        Функция-фильтр, возвращающая True если курс <= max_price
    """
    def filter_fn(course: Course) -> bool:
        return course.calculate() <= max_price
    filter_fn.__doc__ = f"Фильтр: стоимость <= {max_price}"
    return filter_fn


def make_min_students_filter(min_students: int) -> Callable[[Course], bool]:
    """
    Фабрика функций: создаёт фильтр по минимальному количеству студентов
    
    Args:
        min_students: минимальное количество студентов
    
    Returns:
        Функция-фильтр, возвращающая True если студентов >= min_students
    """
    def filter_fn(course: Course) -> bool:
        return course.students_count >= min_students
    filter_fn.__doc__ = f"Фильтр: студентов >= {min_students}"
    return filter_fn


def make_hours_range_filter(min_hours: int, max_hours: int) -> Callable[[Course], bool]:
    """
    Фабрика функций: создаёт фильтр по диапазону часов
    
    Args:
        min_hours: минимальное количество часов
        max_hours: максимальное количество часов
    
    Returns:
        Функция-фильтр, возвращающая True если часы в заданном диапазоне
    """
    def filter_fn(course: Course) -> bool:
        return min_hours <= course.hours <= max_hours
    filter_fn.__doc__ = f"Фильтр: {min_hours} <= часы <= {max_hours}"
    return filter_fn


def make_type_filter(course_type: type) -> Callable[[Course], bool]:
    """
    Фабрика функций: создаёт фильтр по типу курса
    
    Args:
        course_type: класс курса (ProgrammingCourse, LanguageCourse, BusinessCourse)
    
    Returns:
        Функция-фильтр, возвращающая True для курсов указанного типа
    """
    def filter_fn(course: Course) -> bool:
        return isinstance(course, course_type)
    filter_fn.__doc__ = f"Фильтр: тип курса = {course_type.__name__}"
    return filter_fn


# ==================== CALLABLE-СТРАТЕГИИ (паттерн Стратегия) ====================

class DiscountStrategy:
    """
    Стратегия применения скидки к курсу (callable-объект)
    Создаёт новый объект курса? Нет, возвращает кортеж (курс, цена со скидкой)
    """
    
    def __init__(self, discount_percent: float = 10.0):
        """
        Args:
            discount_percent: процент скидки (0-100)
        """
        if not (0 <= discount_percent <= 100):
            raise ValueError("Процент скидки должен быть от 0 до 100")
        self.discount_percent = discount_percent
    
    def __call__(self, course: Course) -> dict:
        """
        Применяет скидку и возвращает информацию о курсе с новой ценой
        
        Returns:
            Словарь с информацией о курсе и ценой со скидкой
        """
        original_cost = course.calculate()
        discounted_cost = original_cost * (1 - self.discount_percent / 100)
        return {
            'title': course.title,
            'teacher': course.teacher,
            'original_cost': original_cost,
            'discount': f"{self.discount_percent}%",
            'new_cost': round(discounted_cost, 2),
            'type': type(course).__name__
        }


class ActivateStrategy:
    """Стратегия активации курса (callable-объект)"""
    
    def __call__(self, course: Course) -> Course:
        """
        Активирует курс (открывает)
        
        Returns:
            Тот же объект курса после активации
        """
        course.open()
        return course


class UpgradeStrategy:
    """Стратегия улучшения курса (callable-объект) — добавляет студентов"""
    
    def __init__(self, students_to_add: int = 5):
        self.students_to_add = students_to_add
    
    def __call__(self, course: Course) -> Course:
        """
        Добавляет указанное количество студентов на курс
        
        Returns:
            Тот же объект курса
        """
        for _ in range(self.students_to_add):
            try:
                course.add_student()
            except (ValueError, RuntimeError):
                break
        return course


class LabelStrategy:
    """Стратегия создания ярлыка/метки для курса (callable-объект)"""
    
    def __init__(self, prefix: str = "КУРС"):
        self.prefix = prefix
    
    def __call__(self, course: Course) -> str:
        """
        Создаёт ярлык курса в формате: [PREFIX] Title — Cost руб
        
        Returns:
            Строка-ярлык
        """
        return f"[{self.prefix}] {course.title} — {course.calculate()} руб"