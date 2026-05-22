"""
Бизнес-логика приложения для управления коллекцией курсов.
Реализует все операции над курсами через коллекцию OnlineSchool.
"""
from typing import List, Optional, Callable, Any, Dict
from collection import OnlineSchool
from base import Course
from models import ProgrammingCourse, LanguageCourse, BusinessCourse
from exceptions import CourseNotFoundError, DuplicateCourseError, ValidationError
from strategies import (
    by_title, by_teacher, by_cost, by_hours, by_students_count,
    is_active, make_min_students_filter
)
from storage import save_to_json, load_from_json


class CourseManager:
    """
    Основной класс управления коллекцией курсов.
    Инкапсулирует все операции над курсами через OnlineSchool.
    """
    
    def __init__(self) -> None:
        """Инициализация менеджера с пустой коллекцией."""
        self.collection: OnlineSchool = OnlineSchool()
    
    # ============ CRUD операции ============
    
    def add_course(self, course: Course) -> None:
        """
        Добавляет курс в коллекцию.
        
        Args:
            course: объект курса для добавления
            
        Raises:
            DuplicateCourseError: если курс с таким названием и преподавателем уже существует
        """
        try:
            self.collection.add(course)
        except ValueError as e:
            raise DuplicateCourseError(course.title, course.teacher) from e
    
    def create_programming_course(
        self, 
        title: str, 
        teacher: str, 
        hours: int, 
        students_count: int,
        language: str, 
        project_count: int
    ) -> ProgrammingCourse:
        """
        Создаёт и добавляет курс программирования.
        
        Returns:
            созданный курс
        """
        course = ProgrammingCourse(
            title, teacher, hours, students_count, language, project_count
        )
        self.add_course(course)
        return course
    
    def create_language_course(
        self,
        title: str,
        teacher: str,
        hours: int,
        students_count: int,
        language: str,
        level: str
    ) -> LanguageCourse:
        """
        Создаёт и добавляет языковой курс.
        
        Returns:
            созданный курс
        """
        course = LanguageCourse(
            title, teacher, hours, students_count, language, level
        )
        self.add_course(course)
        return course
    
    def create_business_course(
        self,
        title: str,
        teacher: str,
        hours: int,
        students_count: int,
        certificate: bool,
        company_partner: str = ""
    ) -> BusinessCourse:
        """
        Создаёт и добавляет бизнес-курс.
        
        Returns:
            созданный курс
        """
        course = BusinessCourse(
            title, teacher, hours, students_count, certificate, company_partner
        )
        self.add_course(course)
        return course
    
    def remove_course(self, title: str, teacher: str) -> None:
        """
        Удаляет курс по названию и преподавателю.
        
        Args:
            title: название курса
            teacher: имя преподавателя
            
        Raises:
            CourseNotFoundError: если курс не найден
        """
        course = self.find_course(title, teacher)
        if course:
            try:
                self.collection.remove(course)
            except ValueError as e:
                raise CourseNotFoundError(f"{title} - {teacher}") from e
        else:
            raise CourseNotFoundError(f"{title} - {teacher}")
    
    def find_course(self, title: str, teacher: Optional[str] = None) -> Optional[Course]:
        """
        Находит курс по названию и опционально по преподавателю.
        
        Args:
            title: название курса
            teacher: имя преподавателя (опционально)
            
        Returns:
            найденный курс или None
        """
        if teacher:
            for course in self.collection:
                if course.title.lower() == title.lower() and course.teacher.lower() == teacher.lower():
                    return course
            return None
        else:
            return self.collection.find_by_title(title)
    
    def get_all_courses(self) -> List[Course]:
        """
        Возвращает все курсы из коллекции.
        
        Returns:
            список всех курсов
        """
        return self.collection.get_all()
    
    def get_course_count(self) -> int:
        """
        Возвращает количество курсов в коллекции.
        
        Returns:
            количество курсов
        """
        return len(self.collection)
    
    # ============ Поиск и фильтрация ============
    
    def search_by_title(self, query: str) -> List[Course]:
        """
        Поиск курсов по части названия.
        
        Args:
            query: поисковый запрос
            
        Returns:
            список найденных курсов
        """
        return self.collection.find_by_title_contains(query)
    
    def filter_courses(self, predicate: Callable[[Course], bool]) -> List[Course]:
        """
        Фильтрация курсов по произвольному предикату.
        
        Args:
            predicate: функция-фильтр
            
        Returns:
            отфильтрованный список курсов
        """
        return self.collection.filter_by(predicate).get_all()
    
    def filter_by_price_range(self, min_price: float, max_price: float) -> List[Course]:
        """
        Фильтрация курсов по диапазону цен.
        
        Args:
            min_price: минимальная цена
            max_price: максимальная цена
            
        Returns:
            курсы в заданном ценовом диапазоне
        """
        return self.filter_courses(
            lambda c: min_price <= c.calculate() <= max_price
        )
    
    def filter_by_type(self, course_type: str) -> List[Course]:
        """
        Фильтрация курсов по типу.
        
        Args:
            course_type: тип курса (programming/language/business)
            
        Returns:
            курсы указанного типа
        """
        type_map = {
            'programming': ProgrammingCourse,
            'language': LanguageCourse,
            'business': BusinessCourse
        }
        
        if course_type not in type_map:
            raise ValidationError(f"Неизвестный тип курса: {course_type}")
        
        return self.collection.get_by_type(type_map[course_type])
    
    def filter_active_courses(self) -> List[Course]:
        """Возвращает только активные курсы."""
        return self.collection.find_active()
    
    # ============ Сортировка ============
    
    def sort_by_title(self) -> List[Course]:
        """Сортировка по названию (алфавитный порядок)."""
        self.collection.sort_by_title()
        return self.collection.get_all()
    
    def sort_by_cost(self) -> List[Course]:
        """Сортировка по стоимости (по возрастанию)."""
        self.collection.sort_by_cost()
        return self.collection.get_all()
    
    def sort_by_hours(self) -> List[Course]:
        """Сортировка по часам (по возрастанию)."""
        sorted_collection = self.collection.sort_by(by_hours)
        return sorted_collection.get_all()
    
    def sort_by_students(self) -> List[Course]:
        """Сортировка по количеству студентов (по возрастанию)."""
        sorted_collection = self.collection.sort_by(by_students_count)
        return sorted_collection.get_all()
    
    def sort_by_teacher(self) -> List[Course]:
        """Сортировка по преподавателю (алфавитный порядок)."""
        sorted_collection = self.collection.sort_by(by_teacher)
        return sorted_collection.get_all()
    
    # ============ Сохранение и загрузка ============
    
    def to_dict_list(self) -> List[Dict[str, Any]]:
        """
        Преобразует все курсы в список словарей для сериализации.
        
        Returns:
            список словарей с данными курсов
        """
        result = []
        for course in self.collection:
            course_dict = {
                'type': type(course).__name__,
                'title': course.title,
                'teacher': course.teacher,
                'hours': course.hours,
                'students_count': course.students_count
            }
            
            if isinstance(course, ProgrammingCourse):
                course_dict['language'] = course.language
                course_dict['project_count'] = course.project_count
            elif isinstance(course, LanguageCourse):
                course_dict['language'] = course.language
                course_dict['level'] = course.level
            elif isinstance(course, BusinessCourse):
                course_dict['certificate'] = course.certificate
                course_dict['company_partner'] = course.company_partner or ""
            
            result.append(course_dict)
        
        return result
    
    def save_to_file(self, filepath: str = None) -> None:
        """
        Сохраняет все курсы в JSON-файл.
        
        Args:
            filepath: путь к файлу
        """
        data = self.to_dict_list()
        save_to_json(data, filepath)
    
    def load_from_file(self, filepath: str = None) -> None:
        """
        Загружает курсы из JSON-файла. Очищает текущую коллекцию перед загрузкой.
        
        Args:
            filepath: путь к файлу
        """
        data = load_from_json(filepath)
        self.collection.clear()
        
        for course_data in data:
            try:
                course_type = course_data['type']
                if course_type == 'ProgrammingCourse':
                    course = ProgrammingCourse(
                        course_data['title'],
                        course_data['teacher'],
                        course_data['hours'],
                        course_data['students_count'],
                        course_data['language'],
                        course_data['project_count']
                    )
                elif course_type == 'LanguageCourse':
                    course = LanguageCourse(
                        course_data['title'],
                        course_data['teacher'],
                        course_data['hours'],
                        course_data['students_count'],
                        course_data['language'],
                        course_data['level']
                    )
                elif course_type == 'BusinessCourse':
                    course = BusinessCourse(
                        course_data['title'],
                        course_data['teacher'],
                        course_data['hours'],
                        course_data['students_count'],
                        course_data['certificate'],
                        course_data.get('company_partner', '')
                    )
                else:
                    continue
                
                self.collection.add(course)
            except Exception as e:
                print(f"Ошибка загрузки курса {course_data.get('title', 'неизвестный')}: {e}")