import json

from .catalog import Catalog
from .entity import Book
from .errors import BadFileError, UnsupportedVersionError

VERSION = 1


def save(catalog, path):
    # сохранение каталога в JSON
    items = []
    for book in catalog:
        items.append(book.to_dict())
    data = {
        'version': VERSION,
        'items': items
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load(path):
    # загрузка каталога, атомарная — при ошибке каталог не меняется
    catalog = Catalog()
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, ValueError) as er:
        raise BadFileError(f'corrupted file: {er}')
    # проверка версии
    if 'version' not in data:
        raise UnsupportedVersionError('missing version')
    if data['version'] != VERSION:
        raise UnsupportedVersionError(
            f'unsupported version: {data["version"]}, expected {VERSION}'
        )
    # десериализация каждого элемента
    try:
        for item_data in data['items']:
            book = Book.from_dict(item_data)
            catalog.add(book)
    except (KeyError, TypeError) as er:
        raise BadFileError(f'corrupted file: {er}')
    return catalog
