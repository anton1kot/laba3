import pytest

from books_catalog.catalog import Catalog
from books_catalog.entity import Book
from books_catalog.errors import DuplicateIdError, NotFoundError


def test_add():
    # успешное добавление книги
    catalog = Catalog()
    book = Book('BK-001', 'Война и мир', 'роман', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09')
    catalog.add(book)
    assert len(catalog) == 1


def test_add_duplicate():
    # добавление дубликата ID → DuplicateIdError
    catalog = Catalog()
    book1 = Book('BK-001', 'Война и мир', 'роман', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09')
    book2 = Book('BK-001', 'Преступление и наказание', 'роман', 1866, 'Ф.М. Достоевский', 'ISBN-978-5-17-08')
    catalog.add(book1)
    with pytest.raises(DuplicateIdError):
        catalog.add(book2)


def test_get():
    # O(1) получение по ID
    catalog = Catalog()
    book = Book('BK-001', 'Война и мир', 'роман', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09')
    catalog.add(book)
    result = catalog.get('BK-001')
    assert result.id == 'BK-001'


def test_get_not_found():
    # получение отсутствующего ID → NotFoundError
    catalog = Catalog()
    with pytest.raises(NotFoundError):
        catalog.get('BK-999')


def test_remove():
    # успешное удаление
    catalog = Catalog()
    book = Book('BK-001', 'Война и мир', 'роман', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09')
    catalog.add(book)
    catalog.remove('BK-001')
    assert len(catalog) == 0


def test_remove_not_found():
    # удаление отсутствующего ID → NotFoundError
    catalog = Catalog()
    with pytest.raises(NotFoundError):
        catalog.remove('BK-999')


def test_remove_updates_index():
    # после удаления get не находит
    catalog = Catalog()
    book = Book('BK-001', 'Война и мир', 'роман', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09')
    catalog.add(book)
    catalog.remove('BK-001')
    with pytest.raises(NotFoundError):
        catalog.get('BK-001')


def test_find_by_category():
    # поиск по категории
    catalog = Catalog()
    b1 = Book('BK-001', 'Война и мир', 'роман', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09')
    b2 = Book('BK-002', 'Евгений Онегин', 'поэзия', 1833, 'А.С. Пушкин', 'ISBN-978-5-17-07')
    b3 = Book('BK-003', 'Анна Каренина', 'роман', 1877, 'Л.Н. Толстой', 'ISBN-978-5-17-06')
    catalog.add(b1)
    catalog.add(b2)
    catalog.add(b3)
    result = catalog.find_by_category('роман')
    assert len(result) == 2


def test_find_by_name_case():
    # поиск по имени нечувствителен к регистру
    catalog = Catalog()
    book = Book('BK-001', 'Война и мир', 'роман', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09')
    catalog.add(book)
    result_lower = catalog.find_by_name('война')
    result_upper = catalog.find_by_name('ВОЙНА')
    result_mixed = catalog.find_by_name('ВоЙнА')
    assert len(result_lower) == 1
    assert len(result_upper) == 1
    assert len(result_mixed) == 1


def test_find_returns_copy():
    # find возвращает копию (нельзя мутировать внутренний список)
    catalog = Catalog()
    book = Book('BK-001', 'Война и мир', 'роман', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09')
    catalog.add(book)
    result = catalog.find_by_category('роман')
    result.clear()
    # после очистки результата каталог не должен измениться
    assert len(catalog) == 1


def test_len():
    # len возвращает количество книг
    catalog = Catalog()
    assert len(catalog) == 0
    catalog.add(Book('BK-001', 'Война и мир', 'роман', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09'))
    catalog.add(Book('BK-002', 'Евгений Онегин', 'поэзия', 1833, 'А.С. Пушкин', 'ISBN-978-5-17-07'))
    assert len(catalog) == 2


def test_iter_deterministic():
    # порядок итерации детерминирован (два раза — одинаковый результат)
    catalog = Catalog()
    b1 = Book('BK-001', 'Война и мир', 'роман', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09')
    b2 = Book('BK-002', 'Евгений Онегин', 'поэзия', 1833, 'А.С. Пушкин', 'ISBN-978-5-17-07')
    b3 = Book('BK-003', 'Мёртвые души', 'поэма', 1842, 'Н.В. Гоголь', 'ISBN-978-5-17-06')
    catalog.add(b1)
    catalog.add(b2)
    catalog.add(b3)
    first_run = [book.id for book in catalog]
    second_run = [book.id for book in catalog]
    assert first_run == second_run
    assert first_run == ['BK-001', 'BK-002', 'BK-003']


def test_contains():
    # проверка наличия ID через __contains__
    catalog = Catalog()
    book = Book('BK-001', 'Война и мир', 'роман', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09')
    catalog.add(book)
    assert 'BK-001' in catalog
    assert 'BK-999' not in catalog
