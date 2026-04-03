from typing import Optional, List, Callable
from model import Course

class OnlineSchool:
    def __init__(self):
        self._items: List[Course] = []
    
    def add(self, course: Course) -> None:

        if not isinstance(course, Course):
            raise TypeError(f"Можно добавлять только объекты Course, получен {type(course).__name__}")
        
        # Проверка на дубликат
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
    
    
    def __len__(self) -> int:
        """Возвращает количество курсов в коллекции"""
        return len(self._items)
    
    def __iter__(self):
        """Позволяет итерироваться по коллекции"""
        return iter(self._items)
    
    
    def __getitem__(self, index: int) -> Course:
        """Поддержка индексации collection[index]"""
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона (0..{len(self._items)-1})")
        return self._items[index]
    
    def sort(self, key: Optional[Callable[[Course], any]] = None, reverse: bool = False) -> None:
        """
        Сортировка коллекции по ключу.
        Примеры:
            collection.sort(key=lambda c: c.title)  # по названию
            collection.sort(key=lambda c: c.hours)  # по часам
            collection.sort(key=lambda c: c.students_count)  # по количеству студентов
        """
        if key is None:
            # Сортировка по умолчанию: по названию, затем по преподавателю
            self._items.sort(key=lambda c: (c.title, c.teacher), reverse=reverse)
        else:
            self._items.sort(key=key, reverse=reverse)
    
    def sort_by_title(self, reverse: bool = False) -> None:
        """Сортировка по названию курса"""
        self.sort(key=lambda c: c.title, reverse=reverse)
    
    def sort_by_teacher(self, reverse: bool = False) -> None:
        """Сортировка по преподавателю"""
        self.sort(key=lambda c: c.teacher, reverse=reverse)
    
    def sort_by_hours(self, reverse: bool = False) -> None:
        """Сортировка по количеству часов"""
        self.sort(key=lambda c: c.hours, reverse=reverse)
    
    def sort_by_students_count(self, reverse: bool = False) -> None:
        """Сортировка по количеству студентов"""
        self.sort(key=lambda c: c.students_count, reverse=reverse)
    
    
    def get_active_courses(self) -> 'OnlineSchool':
        """Вернуть новую коллекцию только с активными курсами"""
        new_collection = OnlineSchool()
        for course in self._items:
            if course.active:
                new_collection.add(course)
        return new_collection
    
    def get_closed_courses(self) -> 'OnlineSchool':
        """Вернуть новую коллекцию только с закрытыми курсами"""
        new_collection = OnlineSchool()
        for course in self._items:
            if not course.active:
                new_collection.add(course)
        return new_collection
    
    def get_courses_with_students(self, min_students: int = 0, max_students: int = Course.MAX_STUDENTS) -> 'OnlineSchool':
        """Вернуть новую коллекцию курсов с количеством студентов в заданном диапазоне"""
        new_collection = OnlineSchool()
        for course in self._items:
            if min_students <= course.students_count <= max_students:
                new_collection.add(course)
        return new_collection
    
    def get_courses_by_hours_range(self, min_hours: int, max_hours: int) -> 'OnlineSchool':
        """Вернуть новую коллекцию курсов с часами в заданном диапазоне"""
        new_collection = OnlineSchool()
        for course in self._items:
            if min_hours <= course.hours <= max_hours:
                new_collection.add(course)
        return new_collection
    
    
    def clear(self) -> None:
        """Очистить коллекцию"""
        self._items.clear()
    
    def is_empty(self) -> bool:
        """Проверить, пуста ли коллекция"""
        return len(self._items) == 0
    
    def __str__(self) -> str:
        """Красивый вывод коллекции"""
        if not self._items:
            return "OnlineSchool (пусто)"
        result = f"OnlineSchool ({len(self._items)} курсов):\n"
        for i, course in enumerate(self._items):
            result += f"  [{i}] {course.title} — {course.teacher} ({course.hours}ч, студентов: {course.students_count})\n"
        return result
    
    def __repr__(self) -> str:
        return f"OnlineSchool({self._items})"