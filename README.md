# Books Service

A minimal CRUD REST API for books, built with [FastAPI](https://fastapi.tiangolo.com/) and managed with [uv](https://docs.astral.sh/uv/).

Books are kept **in memory** (a plain Python dict) — there is no database. All data is lost when the process restarts, which makes this project ideal for learning, prototyping, and demos.

## Features

- Full CRUD: create, list, read, partially update, and delete books
- In-memory storage — zero setup, no database required
- Pydantic validation on every request (422 on bad input)
- Consistent error responses (404 for missing books)
- Interactive Swagger docs at `/docs` and ReDoc at `/redoc`
- Fast, reproducible environment management with `uv`

## Project structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py        # FastAPI app and route handlers
│   ├── schemas.py     # Pydantic request/response models
│   └── store.py       # In-memory data store (the "database")
├── pyproject.toml     # Project metadata and dependencies (managed by uv)
├── .python-version    # Pinned Python version
└── README.md
```

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- No other prerequisites — `uv` downloads and manages Python for you.

## Quick start

```bash
# 1. Install dependencies into .venv (creates the lockfile if missing)
uv sync

# 2. Run the server (with auto-reload)
uv run uvicorn app.main:app --reload
```

The API is now available at <http://127.0.0.1:8000>.

Useful commands:

```bash
uv add <package>            # add a dependency
uv remove <package>         # remove a dependency
uv run books-service        # run the server via the [project.scripts] entrypoint
uv run uvicorn app.main:app --port 9000   # run on a custom port
```

## API reference

Base URL: `http://127.0.0.1:8000`

### Book schema

| Field         | Type          | Required | Notes                          |
| ------------- | ------------- | -------- | ------------------------------ |
| `id`          | `int`         | —        | Assigned by the server         |
| `title`       | `str`         | Yes      | 1–300 characters               |
| `author`      | `str`         | Yes      | 1–200 characters               |
| `description` | `str \| null` | No       | Max 2000 characters            |
| `year`        | `int \| null` | No       | 0–2100                         |
| `created_at`  | `datetime`    | —        | Set on create (UTC)            |
| `updated_at`  | `datetime`    | —        | Refreshed on every update      |

---

### `GET /health`

Liveness probe.

```bash
curl http://127.0.0.1:8000/health
```

```json
{ "status": "ok" }
```

---

### `GET /books`

List all books.

```bash
curl http://127.0.0.1:8000/books
```

`200 OK`

```json
[
  {
    "title": "The Pragmatic Programmer",
    "author": "David Thomas",
    "description": "A classic guide to software craftsmanship.",
    "year": 1999,
    "id": 1,
    "created_at": "2026-10-18T03:39:46.357597Z",
    "updated_at": "2026-10-18T03:39:46.357597Z"
  }
]
```

---

### `POST /books`

Create a new book.

```bash
curl -X POST http://127.0.0.1:8000/books \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "The Pragmatic Programmer",
    "author": "David Thomas",
    "description": "A classic guide to software craftsmanship.",
    "year": 1999
  }'
```

`201 Created`

```json
{
  "title": "The Pragmatic Programmer",
  "author": "David Thomas",
  "description": "A classic guide to software craftsmanship.",
  "year": 1999,
  "id": 1,
  "created_at": "2026-10-18T03:39:46.357597Z",
  "updated_at": "2026-10-18T03:39:46.357597Z"
}
```

`422 Unprocessable Entity` — if the payload is invalid, e.g. missing `author`:

```json
{
  "detail": [
    { "type": "missing", "loc": ["body", "author"], "msg": "Field required", "input": { "title": "No Author Book" } }
  ]
}
```

---

### `GET /books/{id}`

Fetch a single book by id.

```bash
curl http://127.0.0.1:8000/books/1
```

`200 OK` — returns the book.

`404 Not Found` — if the id does not exist:

```json
{ "detail": "Book 999 not found" }
```

---

### `PATCH /books/{id}`

Partially update a book. Only the fields you send are changed; omitted fields keep their current values.

```bash
curl -X PATCH http://127.0.0.1:8000/books/1 \
  -H 'Content-Type: application/json' \
  -d '{ "title": "The Pragmatic Programmer 20th Anniversary" }'
```

`200 OK`

```json
{
  "title": "The Pragmatic Programmer 20th Anniversary",
  "author": "David Thomas",
  "description": "A classic guide to software craftsmanship.",
  "year": 1999,
  "id": 1,
  "created_at": "2026-10-18T03:39:46.357597Z",
  "updated_at": "2026-10-18T03:39:51.892588Z"
}
```

`404 Not Found` — if the id does not exist.

---

### `DELETE /books/{id}`

Delete a book by id.

```bash
curl -X DELETE http://127.0.0.1:8000/books/1
```

`204 No Content` — deleted, empty response body.

`404 Not Found` — if the id does not exist:

```json
{ "detail": "Book 1 not found" }
```

---

### Status code summary

| Code | Meaning                        |
| ---- | ------------------------------ |
| 200  | Request succeeded              |
| 201  | Book created                   |
| 204  | Book deleted                   |
| 404  | Book id not found              |
| 422  | Invalid request payload        |

## Interactive documentation

FastAPI ships with auto-generated docs:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
- OpenAPI schema: <http://127.0.0.1:8000/openapi.json>

## Note on storage

The store is a module-level dict in `app/store.py`. It is single-process and not thread-safe for concurrent writes — perfectly fine for development and demos, but if you outgrow it, swap the `store` module for a real database (e.g. SQLModel + SQLite) without touching the route handlers.
