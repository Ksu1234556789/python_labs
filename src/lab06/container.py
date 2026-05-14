"""
ЛР-6 — Generics и typing
TypedCollection — типизированная версия коллекции из ЛР-2
"""

from typing import (
    TypeVar,
    Generic,
    Callable,
    Optional,
    Protocol,
    runtime_checkable,
    Iterator
)

# ==================== TypeVar ====================

T = TypeVar('T')
R = TypeVar('R')

# ==================== Протоколы ====================

@runtime_checkable
class Displayable(Protocol):
    """Объект умеет отображать себя в строку"""

    def display(self) -> str:
        ...


@runtime_checkable
class Scorable(Protocol):
    """Объект умеет возвращать числовую оценку"""

    def score(self) -> float:
        ...


# Ограниченные TypeVar
D = TypeVar('D', bound=Displayable)
S = TypeVar('S', bound=Scorable)

# ==================== TypedCollection ====================

class TypedCollection(Generic[T]):
    """
    Универсальная типизированная коллекция.
    """

    def __init__(self) -> None:
        self._items: list[T] = []

    # ========== Базовые методы ==========

    def add(self, item: T) -> None:
        """Добавить элемент"""

        if item is None:
            raise TypeError("Нельзя добавить None")

        self._items.append(item)

    def remove(self, item: T) -> None:
        """Удалить элемент"""

        if item not in self._items:
            raise ValueError("Элемент не найден")

        self._items.remove(item)

    def remove_at(self, index: int) -> None:
        """Удалить элемент по индексу"""

        if index < 0 or index >= len(self._items):
            raise IndexError(
                f"Индекс {index} вне диапазона"
            )

        del self._items[index]

    def clear(self) -> None:
        """Очистить коллекцию"""

        self._items.clear()

    def is_empty(self) -> bool:
        """Проверить пустоту"""

        return len(self._items) == 0

    def get_all(self) -> list[T]:
        """Получить копию элементов"""

        return list(self._items)

    # ========== find / filter / map ==========

    def find(
        self,
        predicate: Callable[[T], bool]
    ) -> Optional[T]:
        """
        Найти первый подходящий элемент
        """

        for item in self._items:
            if predicate(item):
                return item

        return None

    def filter(
        self,
        predicate: Callable[[T], bool]
    ) -> list[T]:
        """
        Получить все подходящие элементы
        """

        return [
            item
            for item in self._items
            if predicate(item)
        ]

    def map(
        self,
        transform: Callable[[T], R]
    ) -> list[R]:
        """
        Преобразовать элементы в другой тип
        """

        return [
            transform(item)
            for item in self._items
        ]

    # ========== Magic methods ==========

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)

    def __getitem__(self, index: int) -> T:

        if index < 0 or index >= len(self._items):
            raise IndexError(
                f"Индекс {index} вне диапазона"
            )

        return self._items[index]

    def __str__(self) -> str:

        if not self._items:
            return "TypedCollection(пусто)"

        result = "TypedCollection:\n"

        for i, item in enumerate(self._items):
            result += f"  [{i}] {item}\n"

        return result

    def __repr__(self) -> str:
        return f"TypedCollection({self._items})"


# ==================== DisplayableCollection ====================

class DisplayableCollection(
    TypedCollection[D],
    Generic[D]
):
    """
    Коллекция объектов с display()
    """

    def display_all(self) -> None:
        """
        Вызвать display() у всех элементов
        """

        for item in self._items:
            print(item.display())


# ==================== ScorableCollection ====================

class ScorableCollection(
    TypedCollection[S],
    Generic[S]
):
    """
    Коллекция объектов с score()
    """

    def get_scores(self) -> list[float]:
        """
        Получить оценки всех элементов
        """

        return [
            item.score()
            for item in self._items
        ]

    def get_average_score(self) -> float:
        """
        Средняя оценка
        """

        scores = self.get_scores()

        if not scores:
            return 0.0

        return sum(scores) / len(scores)


# ==================== Тестовые классы ====================

class Student:
    """
    Подходит под Displayable
    """

    def __init__(
        self,
        name: str,
        gpa: float
    ) -> None:

        self.name: str = name
        self.gpa: float = gpa

    def display(self) -> str:
        return (
            f"Студент: {self.name}, GPA: {self.gpa}"
        )

    def __str__(self) -> str:
        return self.display()


class Exam:
    """
    Подходит под Scorable
    """

    def __init__(
        self,
        subject: str,
        points: float
    ) -> None:

        self.subject: str = subject
        self.points: float = points

    def score(self) -> float:
        return self.points

    def __str__(self) -> str:
        return (
            f"Экзамен: {self.subject}, "
            f"баллы: {self.points}"
        )