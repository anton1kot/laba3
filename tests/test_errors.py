import pytest

from src.books_catalog.errors import (
    BooksCatalogError,
    BadFileError,
    DuplicateIdError,
    InvalidEntityError,
    NotFoundError,
    UnsupportedVersionError,
)


def test_hierarchy():
    # все ошибки — подклассы BooksCatalogError
    assert issubclass(InvalidEntityError, BooksCatalogError)
    assert issubclass(DuplicateIdError, BooksCatalogError)
    assert issubclass(NotFoundError, BooksCatalogError)
    assert issubclass(UnsupportedVersionError, BooksCatalogError)
    assert issubclass(BadFileError, BooksCatalogError)
