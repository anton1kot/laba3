# laba3
## Каталог библиотечных книг.

## Возможности

- `add` — добавление книги в каталог
- `get` — получение книги по ID
- `remove` — удаление книги по ID
- `find` — поиск по категории
- `search` — поиск по названию (регистронезависимый)
- `list` — вывод всех книг
- `save` — сохранение каталога в JSON
- `load` — загрузка каталога из JSON

## Требования

- Python ≥ 3.12

## Установка и запуск

Из корня проекта:

```
pip install -e .
```

Запуск команд:
```
python -m books_catalog add --id BK-001 --name "Война и мир" --category "роман" --year 1869 --author "Л.Н. Толстой" --isbn "ISBN-978-5-17-09"
python -m books_catalog list
python -m books_catalog save --path books.json
python -m books_catalog load --path books.json
```

Справка:

```
python -m books_catalog --help
```

Тесты
```
python -m pytest 
```

Проверка
```
ruff check .
```

Структура проекта
```
laba3/
├── pyproject.toml
├── README.md
├── src/
│   └── books_catalog/
│       ├── __init__.py
│       ├── __main__.py      # точка входа CLI
│       ├── entity.py         # сущность Book
│       ├── catalog.py        # каталог
│       ├── storage.py        # JSON сохранение/загрузка
│       └── errors.py         # иерархия ошибок
└── tests/
    ├── test_entity.py
    ├── test_catalog.py
    ├── test_storage.py
    ├── test_errors.py
    └── test_cli.py
```

## Особенности реализации
- Сущность — dataclass с проверкой инвариантов в __post_init__
- Вычислительное ядро (функции каталога) не использует input/print
- Вывод ошибок в stderr и завершение с кодом 2, успешное завершение с кодом 0
- Поиск по ID — через словарь (O(1))
- Поиск по имени/категории — линейный проход (O(n))
- Поиск по имени нечувствителен к регистру
- Методы поиска возвращают копию списка, а не внутренний изменяемый
- Загрузка из JSON атомарна — при ошибке каталог не изменяется
- Обработаны ошибки:
  - неверная сущность (пустой id, некорректный year и т.д.)
  - дубликат ID
  - объект не найден
  - неподдерживаемая версия формата
  - повреждённый файл

## API

### Book

```python
from books_catalog.entity import Book

# создание
book = Book('BK-001', 'Война и мир', 'роман', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09')

# сериализация
data = book.to_dict()
# {'id': 'BK-001', 'name': 'Война и мир', 'category': 'роман', 'year': 1869, ...}

# десериализация
book = Book.from_dict(data)
```

Поля: `id`, `name`, `category`, `year`, `author`, `isbn`

### Catalog

```python
from books_catalog.catalog import Catalog
from books_catalog.entity import Book

catalog = Catalog()

# добавление
catalog.add(book)

# получение по ID (O(1))
book = catalog.get('BK-001')

# удаление
catalog.remove('BK-001')

# поиск по категории (O(n))
results = catalog.find_by_category('роман')

# поиск по названию (O(n), регистронезависимо)
results = catalog.find_by_name('война')

# протоколы
len(catalog)          # количество книг
'BK-001' in catalog   # проверка наличия
for book in catalog:  # итерация в порядке добавления
    ...
```

### Storage

```python
from books_catalog.storage import save, load

# сохранение
save(catalog, 'books.json')

# загрузка (атомарная)
catalog = load('books.json')
```

Формат JSON:
```json
{
    "format_version": 1,
    "items": [
        {"id": "BK-001", "name": "...", "category": "...", "year": 1869, "author": "...", "isbn": "..."}
    ]
}
```

### Ошибки

Все ошибки наследуются от `BooksCatalogError`:

```python
from books_catalog.errors import (
    BooksCatalogError,      # базовый
    InvalidEntityError,     # неверная сущность
    DuplicateIdError,       # дубликат ID
    NotFoundError,          # объект не найден
    UnsupportedVersionError, # неподдерживаемая версия формата
    BadFileError            # повреждённый файл
)
```

Перехват всех ошибок пакета:
```python
try:
    catalog.add(book)
except BooksCatalogError as er:
    print(er)
```
