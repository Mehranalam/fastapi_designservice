"""Pydantic models (request/response schemas) for the books API."""

from datetime import datetime

from pydantic import BaseModel, Field


class BookBase(BaseModel):
    """Fields shared by every book representation."""

    title: str = Field(..., min_length=1, max_length=300, examples=["The Pragmatic Programmer"])
    author: str = Field(..., min_length=1, max_length=200, examples=["David Thomas"])
    description: str | None = Field(None, max_length=2000, examples=["A classic guide to software craftsmanship."])
    year: int | None = Field(None, ge=0, le=2100, examples=[1999])


class BookCreate(BookBase):
    """Payload for creating a new book."""


class BookUpdate(BaseModel):
    """Payload for partially updating a book — only provided fields change."""

    title: str | None = Field(None, min_length=1, max_length=300)
    author: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=2000)
    year: int | None = Field(None, ge=0, le=2100)


class Book(BookBase):
    """A book as stored and returned by the API."""

    id: int
    created_at: datetime
    updated_at: datetime


class Error(BaseModel):
    """Standard error body."""

    detail: str
