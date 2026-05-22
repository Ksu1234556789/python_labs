"""
Пользовательские исключения для предметной области управления курсами.
"""

class CourseError(Exception):
    """Базовое исключение для ошибок, связанных с курсами."""
    pass


class CourseNotFoundError(CourseError):
    """Курс не найден в коллекции."""
    
    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(f"Курс с идентификатором '{identifier}' не найден")


class DuplicateCourseError(CourseError):
    """Курс с таким названием и преподавателем уже существует."""
    
    def __init__(self, title: str, teacher: str):
        self.title = title
        self.teacher = teacher
        super().__init__(
            f"Курс '{title}' с преподавателем '{teacher}' уже существует"
        )


class ValidationError(CourseError):
    """Ошибка валидации данных курса."""
    
    def __init__(self, message: str):
        super().__init__(f"Ошибка валидации: {message}")


class StorageError(CourseError):
    """Ошибка при работе с хранилищем данных."""
    
    def __init__(self, message: str):
        super().__init__(f"Ошибка хранилища: {message}")