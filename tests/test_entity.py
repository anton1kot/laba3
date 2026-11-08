import pytest

from src.books_catalog.entity import Book
from src.books_catalog.errors import InvalidEntityError


def test_valid_book():
    # создание корректной книги
    book = Book('BK-001', 'Война и мир', 'роман', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09')
    assert book.id == 'BK-001'
    assert book.name == 'Война и мир'
    assert book.category == 'роман'
    assert book.year == 1869
    assert book.author == 'Л.Н. Толстой'
    assert book.isbn == 'ISBN-978-5-17-09'


def test_invalid_id_empty():
    # создание с пустым id
    with pytest.raises(InvalidEntityError):
        Book('', 'Война и мир', 'роман', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09')


def test_invalid_id_format():
    # создание с id неверного формата
    with pytest.raises(InvalidEntityError):
        Book('BKXXX', 'Война и мир', 'роман', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09')


def test_invalid_name_empty():
    # создание с пустым названием
    with pytest.raises(InvalidEntityError):
        Book('BK-001', '', 'роман', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09')


def test_invalid_category_empty():
    # создание с пустой категорией
    with pytest.raises(InvalidEntityError):
        Book('BK-001', 'Война и мир', '', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09')


def test_invalid_year_before_christmas():
    # создание с year < 0
    with pytest.raises(InvalidEntityError):
        Book('BK-001', 'Война и мир', 'роман', -999, 'Л.Н. Толстой', 'ISBN-978-5-17-09')


def test_invalid_year_future():
    # создание со слишком далёким будущим годом
    with pytest.raises(InvalidEntityError):
        Book('BK-001', 'Война и мир', 'роман', 2067, 'Газан', 'ISBN-228-5-67-69')


def test_invalid_author_empty():
    # создание с пустым автором
    with pytest.raises(InvalidEntityError):
        Book('BK-001', 'Война и мир', 'роман', 1869, '', 'ISBN-978-5-17-09')


def test_invalid_isbn_empty():
    # создание с пустым isbn
    with pytest.raises(InvalidEntityError):
        Book('BK-001', 'Война и мир', 'роман', 1869, 'Л.Н. Толстой', '')


def test_to_dict():
    # сериализация в словарь
    book = Book('BK-001', 'Война и мир', 'роман', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09')
    d = book.to_dict()
    assert d['id'] == 'BK-001'
    assert d['name'] == 'Война и мир'
    assert d['category'] == 'роман'
    assert d['year'] == 1869
    assert d['author'] == 'Л.Н. Толстой'
    assert d['isbn'] == 'ISBN-978-5-17-09'


def test_from_dict():
    # десериализация из словаря
    data = {
        'id': 'BK-001',
        'name': 'Война и мир',
        'category': 'роман',
        'year': 1869,
        'author': 'Л.Н. Толстой',
        'isbn': 'ISBN-978-5-17-09'
    }
    book = Book.from_dict(data)
    assert book.id == 'BK-001'
    assert book.name == 'Война и мир'
    assert book.year == 1869


def test_round_trip():
    # round trip: from_dict -> to_dict
    data = {
        'id': 'BK-002',
        'name': 'Преступление и наказание',
        'category': 'роман',
        'year': 1866,
        'author': 'Ф.М. Достоевский',
        'isbn': 'ISBN-978-5-17-08'
    }
    book = Book.from_dict(data)
    result = book.to_dict()
    assert result == data
