"""
Коллекция для хранения курсов (из ЛР-2) с расширенными методами для ЛР-5
"""
from typing import Optional, List, Callable, Type, TypeVar, Any
from base import Course
from interfaces import Printable, Comparable
from functools import cmp_to_key


T = TypeVar('T', bound=Course)


class OnlineSchool:
    """Коллекция курсов онлайн-школы"""
    
    def __init__(self):
        self._items: List[Course] = []
    
    def add(self, course: Course) -> None:
        """Добавить курс в коллекцию"""
        if not isinstance(course, Course):
            raise TypeError(f"Можно добавлять только объекты Course, получен {type(course).__name__}")
        
        for existing in self._items:
            if existing == course:  
                raise ValueError(f"Курс '{course.title}' (преподаватель: {course.teacher}) уже существует в коллекции")
        
        self._items.append(course)
    
    def remove(self, course: Course) -> None:
        """Удалить курс из коллекции"""
        if course not in self._items:
            raise ValueError(f"Курс '{course.title}' не найден в коллекции")
        self._items.remove(course)
    
    def remove_at(self, index: int) -> None:
        """Удалить курс по индексу"""
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона (0..{len(self._items)-1})")
        del self._items[index]
    
    def get_all(self) -> List[Course]:
        """Вернуть список всех курсов"""
        return self._items.copy()
    
    def find_by_title(self, title: str) -> Optional[Course]:
        """Поиск курса по названию (первое совпадение)"""
        for course in self._items:
            if course.title.lower() == title.lower():
                return course
        return None
    
    def find_by_teacher(self, teacher: str) -> List[Course]:
        """Поиск всех курсов преподавателя"""
        return [course for course in self._items if course.teacher.lower() == teacher.lower()]
    
    def find_by_title_contains(self, substring: str) -> List[Course]:
        """Поиск курсов, содержащих подстроку в названии"""
        return [course for course in self._items if substring.lower() in course.title.lower()]
    
    def find_active(self) -> List[Course]:
        """Найти все активные курсы"""
        return [course for course in self._items if course.active]
    
    # ========== МЕТОДЫ ИЗ ЛР-3 ==========
    
    def get_by_type(self, course_type: Type[T]) -> List[T]:
        """Получить все курсы определённого типа"""
        return [course for course in self._items if isinstance(course, course_type)]
    
    def get_programming_courses(self):
        """Получить все курсы программирования"""
        from models import ProgrammingCourse
        return self.get_by_type(ProgrammingCourse)
    
    def get_language_courses(self):
        """Получить все языковые курсы"""
        from models import LanguageCourse
        return self.get_by_type(LanguageCourse)
    
    def get_business_courses(self):
        """Получить все бизнес-курсы"""
        from models import BusinessCourse
        return self.get_by_type(BusinessCourse)
    
    def filter_by_type(self, course_type: Type[T]) -> 'OnlineSchool':
        """Создать новую коллекцию, содержащую только курсы определённого типа"""
        new_collection = OnlineSchool()
        for course in self._items:
            if isinstance(course, course_type):
                new_collection.add(course)
        return new_collection
    
    def get_statistics_by_type(self) -> dict:
        """Получить статистику по типам курсов"""
        from models import ProgrammingCourse, LanguageCourse, BusinessCourse
        
        stats = {}
        for course_type, type_name in [
            (ProgrammingCourse, "Programming"),
            (LanguageCourse, "Language"),
            (BusinessCourse, "Business")
        ]:
            courses = self.get_by_type(course_type)
            if courses:
                avg_cost = sum(c.calculate() for c in courses) / len(courses)
                avg_students = sum(c.students_count for c in courses) / len(courses)
                stats[type_name] = {
                    "count": len(courses),
                    "avg_cost": avg_cost,
                    "avg_students": avg_students
                }
        return stats
    
    # ========== НОВЫЕ МЕТОДЫ ДЛЯ ЛР-5 ==========
    
    def sort_by(self, key_func: Callable[[Course], Any], reverse: bool = False) -> 'OnlineSchool':
        """
        Сортировка коллекции по функции-ключу (immutable — возвращает новую коллекцию)
        
        Args:
            key_func: функция, извлекающая ключ сортировки из курса
            reverse: обратный порядок сортировки
        
        Returns:
            Новая отсортированная коллекция OnlineSchool
        """
        new_collection = OnlineSchool()
        sorted_items = sorted(self._items, key=key_func, reverse=reverse)
        for item in sorted_items:
            new_collection.add(item)
        return new_collection
    
    def filter_by(self, predicate: Callable[[Course], bool]) -> 'OnlineSchool':
        """
        Фильтрация коллекции по предикату (immutable — возвращает новую коллекцию)
        
        Args:
            predicate: функция-предикат, возвращающая True/False
        
        Returns:
            Новая отфильтрованная коллекция OnlineSchool
        """
        new_collection = OnlineSchool()
        for course in self._items:
            if predicate(course):
                new_collection.add(course)
        return new_collection
    
    def apply(self, func: Callable[[Course], Course]) -> 'OnlineSchool':
        """
        Применить функцию ко всем элементам коллекции (transform strategy).
        Возвращает новую коллекцию.
        """
        new_collection = OnlineSchool()
        for course in self._items:
            new_collection.add(func(course))
        return new_collection

    
    def map(self, func: Callable[[Course], Any]) -> List[Any]:
        """
        Применить функцию преобразования ко всем элементам и вернуть список результатов
        
        Args:
            func: функция преобразования
        
        Returns:
            Список результатов применения func к каждому элементу
        """
        return list(map(func, self._items))
    
    # ==========================================
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __iter__(self):
        return iter(self._items)
    
    def __getitem__(self, index: int) -> Course:
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона (0..{len(self._items)-1})")
        return self._items[index]
    
    def sort(self, key: Optional[Callable[[Course], Any]] = None, reverse: bool = False) -> None:
        """Сортировка коллекции на месте (mutating)"""
        if key is None:
            self._items.sort(key=lambda c: (c.title, c.teacher), reverse=reverse)
        else:
            self._items.sort(key=key, reverse=reverse)
    
    def sort_by_cost(self, reverse: bool = False) -> None:
        """Сортировка по стоимости курса (на месте)"""
        self.sort(key=lambda c: c.calculate(), reverse=reverse)
    
    def sort_by_title(self, reverse: bool = False) -> None:
        """Сортировка по названию курса (на месте)"""
        self.sort(key=lambda c: c.title, reverse=reverse)
    
    def clear(self) -> None:
        """Очистить коллекцию"""
        self._items.clear()
    
    def is_empty(self) -> bool:
        """Проверить, пуста ли коллекция"""
        return len(self._items) == 0
    
    def __str__(self) -> str:
        if not self._items:
            return "OnlineSchool (пусто)"
        result = f"OnlineSchool ({len(self._items)} курсов):\n"
        for i, course in enumerate(self._items):
            result += f"  [{i}] {course.title} — {course.teacher} ({course.hours}ч, студентов: {course.students_count}, стоимость: {course.calculate()} руб)\n"
        return result
    
    def __repr__(self) -> str:
        return f"OnlineSchool({self._items})"
    
    def get_printable(self):
        return [item for item in self._items if isinstance(item, Printable)]
    
    def get_comparable(self):
        return [item for item in self._items if isinstance(item, Comparable)]
    
    def sort_by_comparable(self):
        items = self.get_comparable()
        items.sort(key=cmp_to_key(lambda a, b: a.compare_to(b)))
        return items
    
    def print_all(self):
        for item in self.get_printable():
            print(item.to_string())