# ЛР-6 — Generics и typing

## 1. Цель работы

Цель лабораторной работы — изучить систему аннотаций типов в Python и возможности модуля `typing`.

В ходе работы были изучены:

- аннотации типов для классов и методов;
- обобщённые классы (`Generic`);
- использование `TypeVar`;
- применение `Callable`, `Optional` и `Iterator`;
- структурная типизация через `Protocol`;
- ограничения типов с помощью `bound=`;
- создание типизированной коллекции объектов.

---

# 2. Описание реализованных типов и контейнеров

## TypedCollection

В файле `container.py` реализован универсальный Generic-класс:

```python
class TypedCollection(Generic[T])
```

Коллекция является типизированной версией контейнера из ЛР-2 и хранит элементы определённого типа `T`.

Поддерживаются операции:

- добавление элементов;
- удаление элементов;
- получение списка элементов;
- очистка коллекции;
- поиск элементов;
- фильтрация;
- преобразование элементов через `map()`.

---

## Используемые TypeVar

### T

```python
T = TypeVar('T')
```

Основной универсальный тип элементов коллекции.

---

### R

```python
R = TypeVar('R')
```

Используется в методе `map()`.

Позволяет возвращать список другого типа:

```python
list[str]
list[float]
```

---

### D и S

```python
D = TypeVar('D', bound=Displayable)
S = TypeVar('S', bound=Scorable)
```

TypeVar с ограничениями через `Protocol`.

---

# Protocol и структурная типизация

## Displayable

```python
class Displayable(Protocol):
    def display(self) -> str:
        ...
```

Объект должен поддерживать метод `display()`.

---

## Scorable

```python
class Scorable(Protocol):
    def score(self) -> float:
        ...
```

Объект должен поддерживать метод `score()`.

---

# Специализированные коллекции

## DisplayableCollection

```python
class DisplayableCollection(
    TypedCollection[D]
)
```

Коллекция объектов, поддерживающих `display()`.

Позволяет безопасно вызывать:

```python
item.display()
```

---

## ScorableCollection

```python
class ScorableCollection(
    TypedCollection[S]
)
```

Коллекция объектов, поддерживающих `score()`.

Реализованы методы:

- получение всех оценок;
- вычисление средней оценки.

---

# Соответствие Protocol без наследования

Классы из ЛР-3 не наследуются от `Displayable` и `Scorable` напрямую.

Однако они содержат необходимые методы:

```python
display()
score()
```

Поэтому Python считает их совместимыми с Protocol.

Это демонстрирует принцип структурной типизации (duck typing).

---

# 3. Демонстрация работы

## TypedCollection

Создание типизированной коллекции:

```python
courses: TypedCollection[ProgrammingCourse]
```

Добавление объектов:

```python
courses.add(py)
courses.add(js)
```

Вывод элементов коллекции.

![TypedCollection](/src/images/lab06/6-01.png)
---

## find / filter / map

### find()

Поиск элемента:

```python
found = all_courses.find(
    lambda c: c.students_count > 20
)
```

Продемонстрированы:

- успешный поиск;
- возврат `None`.

---

### filter()

Фильтрация элементов:

```python
expensive = all_courses.filter(
    lambda c: c.calculate() > 5000
)
```

---

### map()

Преобразование элементов:

```python
titles: list[str]
prices: list[float]
```

Продемонстрировано изменение типа результата через второй `TypeVar R`.

![find / filter / map](/src/images/lab06/6-02.png)
---

## Protocol

### DisplayableCollection

В коллекцию добавлены объекты разных типов:

- `ProgrammingCourse`;
- `LanguageCourse`;
- `BusinessCourse`;
- `Student`.

Все объекты поддерживают метод:

```python
display()
```

---

### ScorableCollection

В коллекцию добавлены объекты:

- `ProgrammingCourse`;
- `LanguageCourse`;
- `BusinessCourse`;
- `Exam`.

Все объекты поддерживают:

```python
score()
```

Продемонстрированы:

- получение списка оценок;
- вычисление средней оценки.


![Protocol Сценарии 1 и 2](/src/images/lab06/6-03.png)


---

# 4. Вывод

В ходе лабораторной работы были изучены возможности системы типизации Python.

Были освоены:

- аннотации типов;
- Generic-классы;
- TypeVar;
- Protocol;
- структурная типизация;
- ограничения типов через `bound=`;
- методы `find`, `filter`, `map`.

Использование типизации делает код:

- более безопасным;
- понятным;
- удобным для поддержки;
- удобным для статического анализа через `mypy` и IDE.