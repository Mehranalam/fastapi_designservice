"""In-memory data store for books.

Books live in a plain dict (a module-level variable), so no database is
required. Data is lost whenever the process restarts.
"""

from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timezone

from app.schemas import Book, BookCreate, BookUpdate

# The single "database" for this service.
_books: dict[int, Book] = {}
_next_id: int = 1


def _now() -> datetime:
    return datetime.now(timezone.utc)


def all_books() -> list[Book]:
    """Return every book, oldest id first."""
    print(_books)
    return [_books[i] for i in sorted(_books)]


def get(book_id: int) -> Book | None:
    return _books.get(book_id)


def create(payload: BookCreate) -> Book:
    global _next_id
    now = _now()
    book = Book(id=_next_id, created_at=now, updated_at=now, **payload.model_dump())
    _books[book.id] = book
    _next_id += 1
    return book


def update(book_id: int, payload: BookUpdate) -> Book | None:
    book = _books.get(book_id)
    if book is None:
        return None
    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        return book
    updated = book.model_copy(update={**changes, "updated_at": _now()})
    _books[book_id] = updated
    return updated


def delete(book_id: int) -> bool:
    return _books.pop(book_id, None) is not None
