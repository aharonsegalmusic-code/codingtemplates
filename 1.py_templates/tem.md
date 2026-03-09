Here’s a minimal FastAPI project template with:

- `main.py` – app entrypoint  
- `database.py` – DB engine & session  
- `models.py` – SQLAlchemy models  
- `schemas.py` – Pydantic BaseModel schemas  
- `routers/items.py` – example router

You can copy-paste this as a starting point.

---

## 1. Suggested project structure

```text
your_project/
├─ app/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ database.py
│  ├─ models.py
│  ├─ schemas.py
│  └─ routers/
│     ├─ __init__.py
│     └─ items.py
└─ requirements.txt
```

---

## 2. `database.py` – DB config & session

```python
# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite memory DB for example; change URL as needed
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 3. `models.py` – SQLAlchemy models

```python
# app/models.py
from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
```

---

## 4. `schemas.py` – Pydantic BaseModel schemas

```python
# app/schemas.py
from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None
    is_active: bool = True


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_active: bool | None = None


class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True  # for Pydantic v2; use orm_mode=True for v1
```

> If you’re on Pydantic v1, replace `from_attributes = True` with:
> ```python
> orm_mode = True
> ```

---

## 5. `routers/items.py` – router with basic CRUD

```python
# app/routers/items.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/items",
    tags=["items"],
)


@router.post("/", response_model=schemas.Item, status_code=status.HTTP_201_CREATED)
def create_item(item_in: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(**item_in.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/", response_model=List[schemas.Item])
def list_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()


@router.get("/{item_id}", response_model=schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )
    return item


@router.put("/{item_id}", response_model=schemas.Item)
def update_item(
    item_id: int,
    item_in: schemas.ItemUpdate,
    db: Session = Depends(get_db),
):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )

    update_data = item_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )
    db.delete(item)
    db.commit()
    return None
```

---

## 6. `main.py` – FastAPI app & router include

```python
# app/main.py
from fastapi import FastAPI

from .database import Base, engine
from . import models
from .routers import items as items_router

# Create tables (simple way for small projects / examples)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Template Example")

app.include_router(items_router.router)


@app.get("/", tags=["root"])
def read_root():
    return {"message": "FastAPI template is running"}
```

---

## 7. `requirements.txt` example

```text
fastapi
uvicorn[standard]
sqlalchemy
pydantic
```

---

## 8. Run the app

From the project root:

```bash
uvicorn app.main:app --reload
```

- Open: `http://127.0.0.1:8000/docs` for Swagger UI  
- Test creating and listing `/items`

---

If you tell me:
- whether you want **async SQLAlchemy** or sync is fine, and  
- which DB you’re planning to use (SQLite, PostgreSQL, etc.),  

I can tweak this template specifically for your stack.