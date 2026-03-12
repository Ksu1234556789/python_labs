from model import Course

# Сценарий 1: создание курсов и вывод
print("\n=== СЦЕНАРИЙ 1: создание курсов и вывод ===")
course1 = Course("Python", "Шубкин", 72, 28)
course2 = Course("Java", "Петров", 60, 15)
course3 = Course("C++", "Сидоров", 50, 10)

print(course1)        
print(repr(course2))  
print(course3)

# сравнение курсов
print("Сравнение course1 == course2?:", course1 == course2)


# Сценарий 2: демонстрация валидации
print("\n=== СЦЕНАРИЙ 2: валидация ===")

# корректное изменение количества студентов
course1.students_count = 25
print("Количество студентов после изменения:", course1.students_count)

# превышение лимита студентов
try:
    course1.students_count = 50
except ValueError as e:
    print("Ошибка:", e)

# попытка создать уже существующий курс
try:
    duplicate_course = Course("Python", "Шубкин", 80, 10)
except ValueError as e:
    print("Ошибка при создании курса:", e)

# попытка создать курс с некорректными данными
try:
    bad_course = Course("", "", 5, -1)
except Exception as e:
    print("Ошибка при создании курса:", e)


# Сценарий 3: логические состояния
print("\n=== СЦЕНАРИЙ 3: логические состояния ===")

print("Курс активен:", course1.active)

course1.close()
print("Курс закрыт:", course1)

# попытка добавить студента на закрытый курс
print('Попытка добавить студента на закрытый курс')
try:
    course1.add_student()
except RuntimeError as e:
    print("Ошибка:", e)


# Сценарий 4: изменение состояния
print("\n=== СЦЕНАРИЙ 4: изменение состояния ===")

course1.open()
print("Курс снова открыт:", course1)

course1.add_student()
print("После добавления студента:", course1)


# Сценарий 5: работа с удалением студентов

print("\n=== СЦЕНАРИЙ 5: удаление студентов ===")

course3.remove_student()
print("После удаления студента из course3:", course3)

try:
    empty_course = Course("HTML", "Нумерович", 20, 0)
    empty_course.remove_student()
except ValueError as e:
    print("Ошибка при удалении студента:", e)


# Сценарий 6: создание нескольких курсов для проверки уникальности

print("\n=== СЦЕНАРИЙ 6: проверка уникальности курсов ===")

try:
    Course("Java", "Петров", 70, 5)  # уже существует
except ValueError as e:
    print("Ошибка:", e)

# новый уникальный курс
new_course = Course("Go", "Кузнецов", 40, 10)
print("Создан новый уникальный курс:", new_course)


# Сценарий 7: магические методы

print("\n=== СЦЕНАРИЙ 7: магические методы ===")
print("Пользовательский вывод:", course1)           # __str__
print("Отладочный вывод:", repr(course1))          # __repr__
print("Сравнение course1 и course2:", course1 == course2)  # __eq__
print("Сравнение course1 и нового уникального курса:", course1 == new_course)