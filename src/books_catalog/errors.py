class BooksCatalogError(Exception):
    # базовый класс ошибок
    pass

class UnsupportedVersionError(BooksCatalogError):
    # неподдерживаемая версия формата
    pass

class InvalidEntityError(BooksCatalogError):
    # некорректная сущность
    pass


class DuplicateIdError(BooksCatalogError):
    # дубликат ID
    pass


class NotFoundError(BooksCatalogError):
    # объект не найден
    pass

class BadFileError(BooksCatalogError):
    # повреждённый файл
    pass
