from abc import ABC, abstractmethod


class Printable(ABC):
    """Интерфейс для вывода объекта"""

    @abstractmethod
    def to_string(self) -> str:
        pass


class Comparable(ABC):
    """Интерфейс для сравнения объектов"""

    @abstractmethod
    def compare_to(self, other) -> int:
        """
        -1 если меньше
         0 если равны
         1 если больше
        """
        pass