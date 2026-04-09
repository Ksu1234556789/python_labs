from base import Course


class OnlineCourse(Course):
    def __init__(self, title, teacher, hours, students_count, platform, price):
        super().__init__(title, teacher, hours, students_count)
        self.platform = platform
        self.price = price

    def connect(self):
        return f"Подключение к платформе {self.platform}"

    def calculate(self):
        # стоимость курса
        return self.price * self.students_count

    def __str__(self):
        return f"[ONLINE] {super().__str__()} | платформа: {self.platform}, цена: {self.price}"


class OfflineCourse(Course):
    def __init__(self, title, teacher, hours, students_count, location, room):
        super().__init__(title, teacher, hours, students_count)
        self.location = location
        self.room = room

    def attend(self):
        return f"Посещение занятия в {self.location}, аудитория {self.room}"

    def calculate(self):
        # нагрузка (пример другой логики)
        return self.hours * 2

    def __str__(self):
        return f"[OFFLINE] {super().__str__()} | место: {self.location}, аудитория: {self.room}"