"""FastAPI application for the books service."""

from fastapi import FastAPI, HTTPException, status

from app import store
from app.schemas import Book, BookCreate, BookUpdate

app = FastAPI(
    title="Books Service",
    description="A minimal CRUD API for books, backed by in-memory storage.",
    version="0.1.0",
)


@app.get("/health", tags=["meta"])
def health() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok"}


@app.get("/books", response_model=list[Book], tags=["books"])
def list_books() -> list[Book]:
    """List all books."""
    return store.all_books()


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED, tags=["books"])
def create_book(payload: BookCreate) -> Book:
    """Create a new book and return it with its assigned id."""
    return store.create(payload)


@app.get("/books/{book_id}", response_model=Book, tags=["books"])
def get_book(book_id: int) -> Book:
    """Get a single book by id."""
    book = store.get(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book {book_id} not found")
    return book


@app.patch("/books/{book_id}", response_model=Book, tags=["books"])
def update_book(book_id: int, payload: BookUpdate) -> Book:
    """Partially update a book — only the provided fields are changed."""
    book = store.update(book_id, payload)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book {book_id} not found")
    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["books"])
def delete_book(book_id: int) -> None:
    """Delete a book by id."""
    if not store.delete(book_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book {book_id} not found")
