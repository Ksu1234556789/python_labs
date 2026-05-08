from base import Course
from interfaces import Printable, Comparable


class ProgrammingCourse(Course, Printable, Comparable):

    def __init__(self, title, teacher, hours, students_count, language, project_count):
        super().__init__(title, teacher, hours, students_count)

        self._validate_language(language)
        self._validate_project_count(project_count)

        self._language = language
        self._project_count = project_count

    def _validate_language(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Некорректный язык")

    def _validate_project_count(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Некорректное количество проектов")

    @property
    def language(self):
        return self._language

    def process(self):
        return f"Processing ProgrammingCourse: {self.title}"

    def calculate(self):
        return self.hours * 100 * 1.3 + self._project_count * 500

    # ===== интерфейсы =====

    def to_string(self) -> str:
        return f"[Programming] {self.title} ({self.language}) — {self.calculate()}руб"

    def compare_to(self, other) -> int:
        if not isinstance(other, Course):
            raise TypeError

        return (self.calculate() > other.calculate()) - (self.calculate() < other.calculate())


class LanguageCourse(Course, Printable, Comparable):

    def __init__(self, title, teacher, hours, students_count, language, level):
        super().__init__(title, teacher, hours, students_count)

        self._language = language
        self._level = level

    @property
    def language(self):
        return self._language

    def process(self):
        return f"Processing LanguageCourse: {self.title}"

    def calculate(self):
        return self.hours * 100

    # ===== интерфейсы =====

    def to_string(self) -> str:
        return f"[Language] {self.title} ({self._level}) — {self.calculate()}руб"

    def compare_to(self, other) -> int:
        if not isinstance(other, Course):
            raise TypeError

        return (self.calculate() > other.calculate()) - (self.calculate() < other.calculate())


class BusinessCourse(Course, Printable, Comparable):

    def __init__(self, title, teacher, hours, students_count, certificate):
        super().__init__(title, teacher, hours, students_count)
        self._certificate = certificate

    def process(self):
        return f"Processing BusinessCourse: {self.title}"

    def calculate(self):
        return self.hours * 120

    # ===== интерфейс =====

    def to_string(self) -> str:
        return f"[Business] {self.title} — {self.calculate()}руб"
    
    def compare_to(self, other) -> int:

        if not isinstance(other, Course):
            raise TypeError

        if self.calculate() > other.calculate():
            return 1

        if self.calculate() < other.calculate():
            return -1

        return 0