

class BooksCatalogError(Exception):
    # Базовый класс ошибок пакета books_catalog.
    pass

class InvalidEntityError(BooksCatalogError):
    pass

class DuplicateIdError(BooksCatalogError):
    pass

class NotFoundError(BooksCatalogError):
    pass

class UnsupportedVersionError(BooksCatalogError):
    pass

class CorruptedFileError(BooksCatalogError):
    pass
