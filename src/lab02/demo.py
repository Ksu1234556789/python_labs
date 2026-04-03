from model import Course
from collection import OnlineSchool


def main():
    print("\n" + "=" * 70)
    print("ЛАБОРАТОРНАЯ РАБОТА №2")
    print("Коллекция объектов Course (OnlineSchool)")
    print("=" * 70)

    # ========== ПОДГОТОВКА: создаём курсы ==========
    course1 = Course("Python для начинающих", "Иванов И.И.", 32, 25)
    course2 = Course("Java программирование", "Петров П.П.", 48, 18)
    course3 = Course("Алгоритмы и структуры", "Смирнов А.В.", 64, 28)
    course4 = Course("Web технологии", "Сидоров С.С.", 36, 10)
    course5 = Course("Базы данных", "Кузнецова Е.Н.", 40, 22)
    course6 = Course("Python продвинутый", "Иванов И.И.", 40, 15)

    collection = OnlineSchool()
    for course in [course1, course2, course3, course4, course5, course6]:
        collection.add(course)

    print("\n Создано 6 курсов и добавлено в коллекцию\n")

    # ========== 1. ИНДЕКСАЦИЯ ==========
    print("=" * 70)
    print("1. ИНДЕКСАЦИЯ (collection[index])")
    print("=" * 70)

    print(f"collection[0] → {collection[0].title} — {collection[0].teacher}")
    print(f"collection[2] → {collection[2].title} — {collection[2].teacher}")


    # Удаление по индексу
    print("\n--- Удаление по индексу (remove_at) ---")
    print(f"До удаления: {len(collection)} курсов")
    deleted = collection[3]
    collection.remove_at(3)
    print(f"Удалён курс: {deleted.title}")
    print(f"После удаления: {len(collection)} курсов")

    # ========== 2. СОРТИРОВКА ==========
    print("\n" + "=" * 70)
    print("2. СОРТИРОВКА")
    print("=" * 70)

    # Сортировка по названию
    print("\n--- Сортировка по названию (sort_by_title) ---")
    collection.sort_by_title()
    for i, course in enumerate(collection):
        print(f"  {i}. {course.title}")

    # Сортировка по часам (убывание)
    print("\n--- Сортировка по часам (sort_by_hours, reverse=True) ---")
    collection.sort_by_hours(reverse=True)
    for course in collection:
        print(f"  • {course.title}: {course.hours} часов")

    # Сортировка по преподавателю
    print("\n--- Сортировка по преподавателю (sort_by_teacher) ---")
    collection.sort_by_teacher()
    for course in collection:
        print(f"  • {course.teacher} → {course.title}")

    # Универсальная сортировка
    print("\n--- Универсальная сортировка (по количеству студентов) ---")
    collection.sort(key=lambda c: c.students_count, reverse=True)
    for course in collection:
        print(f"  • {course.title}: {course.students_count} студентов")

    # ========== 3. ФИЛЬТРАЦИЯ (логические операции) ==========
    print("\n" + "=" * 70)
    print("3. ФИЛЬТРАЦИЯ (логические операции)")
    print("=" * 70)

    # Закроем некоторые курсы для демонстрации
    collection[0].close()
    collection[2].close()

    print("\n--- Активные курсы (get_active_courses) ---")
    active = collection.get_active_courses()
    print(f"Найдено активных курсов: {len(active)}")
    for course in active:
        print(f"  ✅ {course.title} (активен)")

    print("\n--- Курсы с количеством студентов от 15 до 25 ---")
    filtered = collection.get_courses_with_students(15, 25)
    for course in filtered:
        print(f"  • {course.title}: {course.students_count} студентов")

    print("\n--- Курсы с часами от 35 до 50 ---")
    filtered_hours = collection.get_courses_by_hours_range(35, 50)
    for course in filtered_hours:
        print(f"  • {course.title}: {course.hours} часов")

    # ========== 4. ТРИ СЦЕНАРИЯ ИСПОЛЬЗОВАНИЯ ==========
    print("\n" + "=" * 70)
    print("4. СЦЕНАРИИ ИСПОЛЬЗОВАНИЯ КОЛЛЕКЦИИ")
    print("=" * 70)

    # СЦЕНАРИЙ 1: Поиск курсов преподавателя
    print("\n СЦЕНАРИЙ 1: Найти все курсы преподавателя")
    teacher_name = "Иванов И.И."
    teacher_courses = collection.find_by_teacher(teacher_name)
    print(f"Курсы преподавателя {teacher_name}:")
    for course in teacher_courses:
        print(f"  • {course.title} ({course.hours}ч, студентов: {course.students_count})")

    # СЦЕНАРИЙ 2: Формирование расписания (только активные курсы, отсортированные по часам)
    print("\n СЦЕНАРИЙ 2: Формирование расписания (активные курсы, по убыванию часов)")
    schedule = collection.get_active_courses()
    schedule.sort(key=lambda c: c.hours, reverse=True)
    print("Расписание активных курсов (от длительных к коротким):")
    for i, course in enumerate(schedule, 1):
        print(f"  {i}. {course.title} — {course.hours} часов, преподаватель: {course.teacher}")

    # СЦЕНАРИЙ 3: Поиск курсов для записи (есть свободные места)
    print("\n СЦЕНАРИЙ 3: Поиск курсов для записи студентов (есть свободные места)")
    print("Курсы, на которые можно записаться:")
    found_any = False
    for course in collection:
        if course.active:
            free_places = course.MAX_STUDENTS - course.students_count
            if free_places > 0:
                print(f"  ✅ {course.title} — свободно {free_places} мест из {course.MAX_STUDENTS}")
                found_any = True
    if not found_any:
        print("  Нет доступных курсов для записи")

    # СЦЕНАРИЙ 4 (дополнительный): Запись студента на курс
    print("\n СЦЕНАРИЙ 4: Запись студента на курс")
    target_course = collection.find_by_title("Python для начинающих")
    if target_course and target_course.active:
        old_count = target_course.students_count
        target_course.add_student()
        print(f"  Студент записан на курс '{target_course.title}'")
        print(f"  Было студентов: {old_count} → Стало: {target_course.students_count}")
    else:
        print("  Курс не найден или закрыт")

    # ========== ИТОГОВАЯ ИНФОРМАЦИЯ ==========
    print("\n" + "=" * 70)
    print('КОЛЛЕКЦИЯ ПОСЛЕ ВСЕХ ИЗМЕНЕНИЙ')
    print("=" * 70)
    print(f"\n  Всего курсов в коллекции: {len(collection)}")
    print(f"  Активных курсов: {len(collection.get_active_courses())}")
    print(f"  Закрытых курсов: {len(collection.get_closed_courses())}")
    print(collection)



if __name__ == "__main__":
    main()