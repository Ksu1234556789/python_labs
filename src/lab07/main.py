"""
Точка входа в приложение управления курсами.
Загружает данные при запуске, сохраняет при выходе.
"""
from app import CourseManager
from cli import CLI


def main() -> None:
    """Главная функция, инициализирующая приложение."""
    # Создаём менеджер курсов
    manager = CourseManager()
    
    # Автозагрузка данных при запуске
    try:
        manager.load_from_file()
        count = manager.get_course_count()
        if count > 0:
            print(f"📂 Загружено курсов: {count}")
        else:
            print("📂 Файл данных пуст или не найден. Начинаем с пустой коллекции.")
    except Exception as e:
        print(f"⚠️ Ошибка загрузки данных: {e}")
        print("📂 Начинаем с пустой коллекции.")
    
    # Запускаем CLI
    cli = CLI(manager)
    cli.run()


if __name__ == "__main__":
    main()