"""
Дочерние классы курсов (ЛР-3)
"""
from base import Course


class ProgrammingCourse(Course):
    """Курс программирования (дочерний класс 1)"""
    
    def __init__(self, title: str, teacher: str, hours: int, students_count: int,
                 language: str, project_count: int):
        """
        Дополнительные атрибуты:
        - language: язык программирования
        - project_count: количество проектов на курсе
        """
        super().__init__(title, teacher, hours, students_count)
        
        # Валидация новых атрибутов
        self._validate_language(language)
        self._validate_project_count(project_count)
        
        self._language = language
        self._project_count = project_count
    
    def _validate_language(self, value):
        if not isinstance(value, str):
            raise TypeError("Язык программирования должен быть строкой")
        if not value.strip():
            raise ValueError("Язык программирования не может быть пустым")
    
    def _validate_project_count(self, value):
        if not isinstance(value, int):
            raise TypeError("Количество проектов должно быть числом")
        if value < 0:
            raise ValueError("Количество проектов не может быть отрицательным")
    
    # Новые атрибуты (properties)
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
    
    # Новый метод
    def add_project(self):
        """Добавить проект к курсу"""
        self._project_count += 1
        return f"Проект добавлен. Всего проектов: {self._project_count}"
    
    # Переопределение абстрактных методов базового класса
    def process(self):
        """Полиморфный метод для курса программирования"""
        status = "активен" if self._active else "закрыт"
        return (f"Обработка курса программирования '{self._title}': "
                f"статус {status}, студентов {self._students_count}, "
                f"язык: {self._language}, проектов: {self._project_count}")
    
    def calculate(self):
        """Расчёт стоимости курса программирования (дороже базового)"""
        base_price = self._hours * 100
        # Наценка за сложность: +30% + бонус за проекты
        project_bonus = self._project_count * 500
        return base_price * 1.3 + project_bonus
    
    def __str__(self):
        base_str = super().__str__()
        return f"[Programming] {base_str} | Язык: {self._language}, проектов: {self._project_count}"
    
    def __repr__(self):
        return (f"ProgrammingCourse(title='{self._title}', teacher='{self._teacher}', "
                f"hours={self._hours}, students_count={self._students_count}, "
                f"language='{self._language}', project_count={self._project_count})")


class LanguageCourse(Course):
    """Языковой курс (дочерний класс 2)"""
    
    VALID_LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
    
    def __init__(self, title: str, teacher: str, hours: int, students_count: int,
                 language: str, level: str):
        """
        Дополнительные атрибуты:
        - language: изучаемый язык
        - level: уровень (A1, A2, B1, B2, C1, C2)
        """
        super().__init__(title, teacher, hours, students_count)
        
        # Валидация новых атрибутов
        self._validate_language(language)
        self._validate_level(level)
        
        self._language = language
        self._level = level
        self._native_speaker = False  # доп. атрибут по умолчанию
    
    def _validate_language(self, value):
        if not isinstance(value, str):
            raise TypeError("Язык должен быть строкой")
        if not value.strip():
            raise ValueError("Язык не может быть пустым")
    
    def _validate_level(self, value):
        if value not in self.VALID_LEVELS:
            raise ValueError(f"Уровень должен быть одним из: {', '.join(self.VALID_LEVELS)}")
    
    # Новые атрибуты (properties)
    @property
    def language(self):
        return self._language
    
    @property
    def level(self):
        return self._level
    
    @level.setter
    def level(self, value):
        self._validate_level(value)
        self._level = value
    
    @property
    def native_speaker(self):
        return self._native_speaker
    
    # Новые методы
    def set_native_speaker(self, is_native: bool):
        """Установить, ведёт ли курс носитель языка"""
        self._native_speaker = is_native
        speaker_type = "носитель языка" if is_native else "не носитель"
        return f"Преподаватель: {speaker_type}"
    
    def upgrade_level(self):
        """Повысить уровень курса"""
        current_index = self.VALID_LEVELS.index(self._level)
        if current_index < len(self.VALID_LEVELS) - 1:
            self._level = self.VALID_LEVELS[current_index + 1]
            return f"Уровень повышен до {self._level}"
        return "Достигнут максимальный уровень C2"
    
    # Переопределение абстрактных методов базового класса
    def process(self):
        """Полиморфный метод для языкового курса"""
        status = "активен" if self._active else "закрыт"
        native_info = " (носитель)" if self._native_speaker else ""
        return (f"Обработка языкового курса '{self._title}': "
                f"статус {status}, студентов {self._students_count}, "
                f"язык: {self._language}, уровень: {self._level}{native_info}")
    
    def calculate(self):
        """Расчёт стоимости языкового курса (зависит от уровня)"""
        base_price = self._hours * 100
        # Коэффициент сложности по уровню
        level_multipliers = {
            'A1': 0.8, 'A2': 0.9,
            'B1': 1.0, 'B2': 1.2,
            'C1': 1.5, 'C2': 2.0
        }
        multiplier = level_multipliers.get(self._level, 1.0)
        # Наценка за носителя языка
        native_bonus = 1.3 if self._native_speaker else 1.0
        return base_price * multiplier * native_bonus
    
    def __str__(self):
        base_str = super().__str__()
        native_str = " (носитель)" if self._native_speaker else ""
        return f"[Language] {base_str} | Язык: {self._language}, уровень: {self._level}{native_str}"
    
    def __repr__(self):
        return (f"LanguageCourse(title='{self._title}', teacher='{self._teacher}', "
                f"hours={self._hours}, students_count={self._students_count}, "
                f"language='{self._language}', level='{self._level}')")


class BusinessCourse(Course):
    """Бизнес-курс (дочерний класс 3 - дополнительный)"""
    
    def __init__(self, title: str, teacher: str, hours: int, students_count: int,
                 certificate: bool, company_partner: str = ""):
        """
        Дополнительные атрибуты:
        - certificate: выдаётся ли сертификат
        - company_partner: компания-партнёр
        """
        super().__init__(title, teacher, hours, students_count)
        
        self._validate_certificate(certificate)
        self._validate_company_partner(company_partner)
        
        self._certificate = certificate
        self._company_partner = company_partner if company_partner else None
    
    def _validate_certificate(self, value):
        if not isinstance(value, bool):
            raise TypeError("certificate должен быть булевым значением")
    
    def _validate_company_partner(self, value):
        if not isinstance(value, str):
            raise TypeError("company_partner должен быть строкой")
    
    # Новые атрибуты (properties)
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
    
    # Новые методы
    def has_partner(self) -> bool:
        """Проверить наличие партнёра"""
        return self._company_partner is not None
    
    def issue_certificate(self):
        """Выдать сертификат (активирует флаг)"""
        self._certificate = True
        return "Сертификат будет выдан по окончании курса"
    
    # Переопределение абстрактных методов базового класса
    def process(self):
        """Полиморфный метод для бизнес-курса"""
        status = "активен" if self._active else "закрыт"
        cert_info = "с сертификатом" if self._certificate else "без сертификата"
        partner_info = f", партнёр: {self._company_partner}" if self._company_partner else ""
        return (f"Обработка бизнес-курса '{self._title}': "
                f"статус {status}, студентов {self._students_count}, "
                f"{cert_info}{partner_info}")
    
    def calculate(self):
        """Расчёт стоимости бизнес-курса (премиум-сегмент)"""
        base_price = self._hours * 100
        # Сертификация добавляет 40% к стоимости
        cert_multiplier = 1.4 if self._certificate else 1.0
        # Партнёрская скидка 15%
        partner_discount = 0.85 if self._company_partner else 1.0
        return base_price * cert_multiplier * partner_discount
    
    def __str__(self):
        base_str = super().__str__()
        cert_str = ", сертификат" if self._certificate else ""
        partner_str = f", партнёр: {self._company_partner}" if self._company_partner else ""
        return f"[Business] {base_str}{cert_str}{partner_str}"
    
    def __repr__(self):
        return (f"BusinessCourse(title='{self._title}', teacher='{self._teacher}', "
                f"hours={self._hours}, students_count={self._students_count}, "
                f"certificate={self._certificate}, company_partner='{self._company_partner}')")