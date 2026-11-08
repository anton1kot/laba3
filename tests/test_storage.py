import json
import os
import tempfile

import pytest

from books_catalog.catalog import Catalog
from books_catalog.entity import Book
from books_catalog.errors import BadFileError, UnsupportedVersionError
from books_catalog.storage import load, save


def test_json_round_trip():
    # save → load = исходный каталог
    catalog = Catalog()
    b1 = Book('BK-001', 'Война и мир', 'роман', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09')
    b2 = Book('BK-002', 'Евгений Онегин', 'поэзия', 1833, 'А.С. Пушкин', 'ISBN-978-5-17-07')
    catalog.add(b1)
    catalog.add(b2)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        tmp_path = f.name

    try:
        save(catalog, tmp_path)
        loaded = load(tmp_path)
        assert len(loaded) == 2
        assert loaded.get('BK-001').name == 'Война и мир'
        assert loaded.get('BK-002').name == 'Евгений Онегин'
    finally:
        os.unlink(tmp_path)


def test_save_preserves_all_fields():
    # сохраняются все поля
    catalog = Catalog()
    book = Book('BK-001', 'Война и мир', 'роман', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09')
    catalog.add(book)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        tmp_path = f.name

    try:
        save(catalog, tmp_path)
        loaded = load(tmp_path)
        b = loaded.get('BK-001')
        assert b.id == 'BK-001'
        assert b.name == 'Война и мир'
        assert b.category == 'роман'
        assert b.year == 1869
        assert b.author == 'Л.Н. Толстой'
        assert b.isbn == 'ISBN-978-5-17-09'
    finally:
        os.unlink(tmp_path)


def test_unsupported_version():
    # неизвестная версия формата → UnsupportedVersionError
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump({'version': 99, 'items': []}, f, ensure_ascii=False)
        tmp_path = f.name

    try:
        with pytest.raises(UnsupportedVersionError):
            load(tmp_path)
    finally:
        os.unlink(tmp_path)


def test_corrupted_json():
    # повреждённый JSON → CorruptedFileError
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        f.write('{not valid json}')
        tmp_path = f.name

    try:
        with pytest.raises(BadFileError):
            load(tmp_path)
    finally:
        os.unlink(tmp_path)


def test_load_atomicity():
    # при ошибке загрузки существующий каталог не изменён
    catalog = Catalog()
    catalog.add(Book('BK-001', 'Война и мир', 'роман', 1869, 'Л.Н. Толстой', 'ISBN-978-5-17-09'))

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump({'version': 99, 'items': []}, f, ensure_ascii=False)
        tmp_path = f.name

    try:
        with pytest.raises(UnsupportedVersionError):
            load(tmp_path)
        # каталог не должен измениться
        assert len(catalog) == 1
        assert catalog.get('BK-001').name == 'Война и мир'
    finally:
        os.unlink(tmp_path)


def test_missing_version():
    # отсутствие version → UnsupportedVersionError
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump({'items': []}, f, ensure_ascii=False)
        tmp_path = f.name

    try:
        with pytest.raises(UnsupportedVersionError):
            load(tmp_path)
    finally:
        os.unlink(tmp_path)
