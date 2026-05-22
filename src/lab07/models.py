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
            raise ValueError("Некорректный язык программирования")

    def _validate_project_count(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Количество проектов должно быть целым неотрицательным числом")

    @property
    def language(self):
        return self._language

    @property
    def project_count(self):
        return self._project_count

    @project_count.setter
    def project_count(self, value):
        self._validate_project_count(value)
        self._project_count = value

    def process(self):
        return f"Processing ProgrammingCourse: {self.title}"

    def calculate(self):
        return self.hours * 100 * 1.3 + self._project_count * 500

    def to_string(self) -> str:
        return f"[Programming] {self.title} ({self.language}) — {self.calculate()}руб"

    def compare_to(self, other) -> int:
        if not isinstance(other, Course):
            raise TypeError
        return (self.calculate() > other.calculate()) - (self.calculate() < other.calculate())


class LanguageCourse(Course, Printable, Comparable):

    VALID_LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'А1', 'А2', 'В1', 'В2', 'С1', 'С2']
    VALID_LANGUAGES = ['Английский', 'Немецкий', 'Французский', 'Испанский', 'Итальянский',
        'Китайский', 'Японский', 'Корейский', 'Русский', 'Арабский',
        'Португальский', 'Турецкий', 'Хинди']

    def __init__(self, title, teacher, hours, students_count, language, level):
        super().__init__(title, teacher, hours, students_count)

        self._validate_language(language)
        self._validate_level(level)

        self._language = language
        self._level = level

    def _validate_language(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Язык не может быть пустым")
        # Опционально: проверка по списку допустимых языков
        # if value.capitalize() not in self.VALID_LANGUAGES:
        #     raise ValueError(f"Язык должен быть одним из: {', '.join(self.VALID_LANGUAGES)}")

    def _validate_level(self, value):
        if not isinstance(value, str):
            raise TypeError("Уровень должен быть строкой")
        if value.upper() not in self.VALID_LEVELS:
            raise ValueError(f"Уровень должен быть одним из: {', '.join(self.VALID_LEVELS)}")

    @property
    def language(self):
        return self._language

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._validate_level(value)
        self._level = value.upper()

    def process(self):
        return f"Processing LanguageCourse: {self.title}"

    def calculate(self):
        return self.hours * 100

    def to_string(self) -> str:
        return f"[Language] {self.title} ({self._level}) — {self.calculate()}руб"

    def compare_to(self, other) -> int:
        if not isinstance(other, Course):
            raise TypeError
        return (self.calculate() > other.calculate()) - (self.calculate() < other.calculate())


class BusinessCourse(Course, Printable, Comparable):

    def __init__(self, title, teacher, hours, students_count, certificate, company_partner=""):
        super().__init__(title, teacher, hours, students_count)
        
        self._validate_certificate(certificate)
        self._validate_company_partner(company_partner)
        
        self._certificate = certificate
        self._company_partner = company_partner if company_partner else None

    def _validate_certificate(self, value):
        if not isinstance(value, bool):
            raise TypeError("Сертификат должен быть булевым значением (True/False)")

    def _validate_company_partner(self, value):
        if not isinstance(value, str):
            raise TypeError("Название компании-партнёра должно быть строкой")
        # Разрешаем пустую строку (нет партнёра)
        # Но если указан — проверяем что не только пробелы
        if value and not value.strip():
            raise ValueError("Название компании-партнёра не может состоять только из пробелов")

    @property
    def certificate(self):
        return self._certificate

    @certificate.setter
    def certificate(self, value):
        self._validate_certificate(value)
        self._certificate = value

    @property
    def company_partner(self):
        return self._company_partner

    @company_partner.setter
    def company_partner(self, value):
        self._validate_company_partner(value)
        self._company_partner = value if value else None

    def process(self):
        return f"Processing BusinessCourse: {self.title}"

    def calculate(self):
        return self.hours * 120

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