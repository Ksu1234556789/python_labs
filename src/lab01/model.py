class Course:
# атрибуты класса 
    MAX_STUDENTS = 30
    MIN_HOURS = 16
    existing_courses = set()

    def __init__(self, title: str, teacher: str, hours: int, students_count: int):
        self._validate_title(title)
        self._validate_teacher(teacher)
        self._validate_hours(hours)
        self._validate_students_count(students_count)

        # проверка на одинаковые курсы
        key = (title, teacher)
        if key in Course.existing_courses:
            raise ValueError("Курс с таким названием и преподавателем уже существует")

        self._title = title
        self._teacher = teacher
        self._hours = hours
        self._students_count = students_count
        self._active = True  # логическое состояние (активный или закрытый курс)

        Course.existing_courses.add(key)

    # валидация
    def _validate_title(self, value):
        if not isinstance(value, str):
            raise TypeError("Название курса должно быть строкой")
        if not value.strip():
            raise ValueError("Название курса не может быть пустым")

    def _validate_teacher(self, value):
        if not isinstance(value, str):
            raise TypeError("Имя преподавателя должно быть строкой")
        if not value.strip():
            raise ValueError("Имя преподавателя не может быть пустым")

    def _validate_hours(self, value):
        if not isinstance(value, int):
            raise TypeError("Часы должны быть числом")
        if value < self.MIN_HOURS:
            raise ValueError(
                f"Часы должны быть не меньше {self.MIN_HOURS}"
            )

    def _validate_students_count(self, value):
        if not isinstance(value, int):
            raise TypeError("Количество студентов должно быть числом")
        if not (0 <= value <= self.MAX_STUDENTS):
            raise ValueError(
                f"Количество студентов должно быть от 0 до {self.MAX_STUDENTS}"
            )

    # property
    @property
    def title(self):
        return self._title

    @property
    def teacher(self):
        return self._teacher

    @property
    def hours(self):
        return self._hours

    @property
    def students_count(self):
        return self._students_count

    @students_count.setter
    def students_count(self, value):
        self._validate_students_count(value)
        self._students_count = value

    @property
    def active(self):
        return self._active

    # бизнес-методы
    def add_student(self):
        if not self._active:
            raise RuntimeError("Нельзя добавить студента: курс закрыт")
        if self._students_count >= self.MAX_STUDENTS:
            raise ValueError("Достигнут лимит студентов")

        self._students_count += 1

    def remove_student(self):
        if self._students_count == 0:
            raise ValueError("Нельзя удалить студента: список пуст")
        self._students_count -= 1

    # изм. состояния
    def close(self):
        self._active = False

    def open(self):
        self._active = True

    # magic methods
    def __str__(self):
        status = "активен" if self._active else "закрыт"
        return (
            f"Курс '{self._title}', "
            f"преподаватель: {self._teacher}, "
            f"часы: {self._hours}, "
            f"студентов: {self._students_count}/{self.MAX_STUDENTS}, "
            f"статус: {status}"
        )

    def __repr__(self):
        return (
            f"Course(title='{self._title}', teacher='{self._teacher}', "
            f"hours={self._hours}, students_count={self._students_count})"
        )

    def __eq__(self, other):
        if not isinstance(other, Course):
            return NotImplemented
        return self._title == other._title and self._teacher == other._teacher