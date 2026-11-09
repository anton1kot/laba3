import sys

from books_catalog.catalog import Catalog
from books_catalog.entity import Book
from books_catalog.errors import (
    BadFileError,
    BooksCatalogError,
    DuplicateIdError,
    InvalidEntityError,
    NotFoundError,
    UnsupportedVersionError,
)
from books_catalog.storage import load, save


class Arguments:
    def __init__(self, argvs):
        if len(argvs) >= 1:
            self.mode = argvs[0]  # команда
            self.args = argvs[1:]
        else:
            self.mode = 'err'
        self.condition = None
        self.options = {}

    def pars(self):
        for arg in self.args:
            if arg.startswith('--'):
                key = arg[2:]
                self.condition = key
                continue
            if self.condition:
                self.options[self.condition] = arg
                self.condition = None


def main():
    args = Arguments(sys.argv[1:])
    args.pars()

    if args.mode == '--help':
        sys.stdout.write('''
Usage:
    python -m books_catalog --help
        Показать справку

    python -m books_catalog add --id ID --name NAME --category CATEGORY --year YEAR --author AUTHOR --isbn ISBN
        Добавить книгу в каталог

    python -m books_catalog get --id ID
        Получить книгу по ID

    python -m books_catalog remove --id ID
        Удалить книгу по ID

    python -m books_catalog find --category CATEGORY
        Найти книги по категории

    python -m books_catalog search --name NAME
        Найти книги по названию

    python -m books_catalog list
        Вывести все книги (итерация в порядке добавления)

    python -m books_catalog save --path PATH
        Сохранить каталог в JSON файл

    python -m books_catalog load --path PATH
        Загрузить каталог из JSON файла
        ''')
        return

    catalog = Catalog()

    # если есть сохранённый файл, загружаем его
    if 'load' in args.mode or 'save' in args.mode:
        if 'path' in args.options:
            catalog = load(args.options['path'])

    if args.mode == 'add':
        book = Book(
            id=args.options.get('id', ''),
            name=args.options.get('name', ''),
            category=args.options.get('category', ''),
            year=int(args.options.get('year', '0')),
            author=args.options.get('author', ''),
            isbn=args.options.get('isbn', '')
        )
        catalog.add(book)
        sys.stdout.write(f'added: {book.id} — {book.name}\n')

    elif args.mode == 'get':
        book = catalog.get(args.options.get('id', ''))
        sys.stdout.write(f'{book.id} | {book.name} | {book.category} | {book.year} | {book.author} | {book.isbn}\n')

    elif args.mode == 'remove':
        catalog.remove(args.options.get('id', ''))
        sys.stdout.write(f'removed: {args.options.get("id", "")}\n')

    elif args.mode == 'find':
        category = args.options.get('category', '')
        results = catalog.find_by_category(category)
        for book in results:
            sys.stdout.write(f'{book.id} | {book.name} | {book.category} | {book.year} | {book.author} | {book.isbn}\n')
        sys.stdout.write(f'found: {len(results)}\n')

    elif args.mode == 'search':
        query = args.options.get('name', '')
        results = catalog.find_by_name(query)
        for book in results:
            sys.stdout.write(f'{book.id} | {book.name} | {book.category} | {book.year} | {book.author} | {book.isbn}\n')
        sys.stdout.write(f'found: {len(results)}\n')

    elif args.mode == 'list':
        for book in catalog:
            sys.stdout.write(f'{book.id} | {book.name} | {book.category} | {book.year} | {book.author} | {book.isbn}\n')
        sys.stdout.write(f'total: {len(catalog)}\n')

    elif args.mode == 'save':
        path = args.options.get('path', '')
        if not path:
            sys.stderr.write('Please specify --path for save')
            sys.exit(2)
        save(catalog, path)
        sys.stdout.write(f'saved: {len(catalog)} books to {path}\n')

    elif args.mode == 'load':
        path = args.options.get('path', '')
        if not path:
            sys.stderr.write('Please specify --path for load')
            sys.exit(2)
        catalog = load(path)
        sys.stdout.write(f'loaded: {len(catalog)} books from {path}\n')

    else:
        sys.stderr.write('Unknown command. For help: python -m books_catalog --help\n')
        sys.exit(2)


if __name__ == '__main__':
    try:
        main()
    except BooksCatalogError as er:
        sys.stderr.write(f'{type(er).__name__}: {er}')
        sys.exit(2)
