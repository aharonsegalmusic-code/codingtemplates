# Python Code Templates & Reusable Patterns

Reusable Python snippets and a full FastAPI project template. Copy-paste starting points for common patterns.

---

## What's here

- `tem.md` — FastAPI + SQLAlchemy reference guide (models, schemas, CRUD, router wiring)
- `class.py` — Python class patterns: inheritance, dunder methods, properties
- `error_handeling.py` — Try/except patterns, custom exceptions, HTTP error raising
- `file_handeling.py` — File read/write/append, CSV and JSON handling
- `pd_template.py` — Pandas: DataFrame creation, filtering, groupby, merge, export
- `html/basic_html.py` — Serving HTML from Python / FastAPI

## fast_api/ — Full FastAPI project template

- `main.py` — App entry point, lifespan, route registration
- `database.py` — SQLAlchemy engine + `get_db()` session generator
- `schemas.py` — Pydantic request/response models (Pydantic v2)
- `router.py` — Route definitions with `APIRouter` and `Depends(get_db)`

**Stack:** FastAPI · SQLAlchemy · Pydantic v2 · SQLite
