from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from pymongo.database import Database

import mongo_overview as mo

router = APIRouter()


def get_db(request: Request) -> Database:
    return request.app.state.mongo.db

"""
DB = Annotated[Database, Depends(get_db)]

Type alias used by FastAPI: when a route parameter is typed as `DB`, FastAPI will call `get_db(...)`
and inject its return value (a PyMongo `Database`) into the endpoint automatically.
"""
DB = Annotated[Database, Depends(get_db)]


@router.get("/collections")
def list_collections(db: DB):
    return {"collections": db.list_collection_names()}


# ----------------------------
# Generic query routes (reuse)
# ----------------------------

@router.get("/find/{collection_name}")
def find_many(
    collection_name: str,
    db: DB,
    field: str | None = None,
    value: str | None = None,
    limit: int = 20,
):
    """
    Examples:
      /find/stores?limit=5
      /find/stores?field=city&value=London&limit=10
    """
    filter_doc = {}
    if field is not None:
        if value is None:
            raise HTTPException(status_code=400, detail="If you pass field, you must pass value too.")
        filter_doc[field] = value

    documents = mo.find_many(db, collection_name, filter=filter_doc, limit=limit)
    return {"documents": documents}


@router.get("/find-one/{collection_name}")
def find_one(
    collection_name: str,
    db: DB,
    field: str | None = None,
    value: str | None = None,
):
    """
    Example:
      /find-one/stores?field=store_id&value=101
    """
    filter_doc = {}
    if field is not None:
        if value is None:
            raise HTTPException(status_code=400, detail="If you pass field, you must pass value too.")
        filter_doc[field] = value

    document = mo.find_one(db, collection_name, filter=filter_doc)
    return {"document": document}


@router.get("/count/{collection_name}")
def count_docs(
    collection_name: str,
    db: DB,
    field: str | None = None,
    value: str | None = None,
):
    """
    Examples:
      /count/customers
      /count/customers?field=country&value=Canada
    """
    filter_doc = {}
    if field is not None:
        if value is None:
            raise HTTPException(status_code=400, detail="If you pass field, you must pass value too.")
        filter_doc[field] = value

    n = mo.count(db, collection_name, filter=filter_doc)
    return {"count": n}


@router.get("/distinct/{collection_name}")
def distinct_values(
    collection_name: str,
    field: str,
    db: DB,
    limit: int = 100,
):
    """
    Example:
      /distinct/purchases?field=category
    """
    values = mo.distinct_values(db, collection_name, field=field, limit=limit)
    return {"values": values}