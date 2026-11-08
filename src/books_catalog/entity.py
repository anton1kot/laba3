from dataclasses import dataclass

from .errors import InvalidEntityError


@dataclass
class Book:
    # сущность — библиотечная книга
    id: str
    name: str
    category: str
    year: int
    author: str
    isbn: str

    def __post_init__(self):
        # проверка id — не пустая, формат BK-XXX
        if not self.id or not self.id.startswith('BK-'):
            raise InvalidEntityError('invalid id format, expected BK-XXX')
        # проверка name — не пустая
        if not self.name or self.name.strip() == '':
            raise InvalidEntityError('name cannot be empty')
        # проверка category — не пустая
        if not self.category or self.category.strip() == '':
            raise InvalidEntityError('category cannot be empty')
        # проверка year — 1 <= year <= 2027
        if self.year < 1 or self.year > 2027:
            raise InvalidEntityError('year must be between 1 and 2027')
        # проверка author — не пустая
        if not self.author or self.author.strip() == '':
            raise InvalidEntityError('author cannot be empty')
        # проверка isbn — не пустая
        if not self.isbn or self.isbn.strip() == '':
            raise InvalidEntityError('isbn cannot be empty')

    def to_dict(self):
        # сериализация в словарь
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'year': self.year,
            'author': self.author,
            'isbn': self.isbn
        }

    @classmethod
    def from_dict(cls, data):
        # десериализация из словаря
        return cls(
            id=data['id'],
            name=data['name'],
            category=data['category'],
            year=data['year'],
            author=data['author'],
            isbn=data['isbn']
        )
