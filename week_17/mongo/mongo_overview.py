from typing import Any, Optional
from pymongo.database import Database


def find_many(
    db: Database,
    collection_name: str,
    filter: Optional[dict[str, Any]] = None,
    projection: Optional[dict[str, int]] = None,
    sort: Optional[list[tuple[str, int]]] = None,
    limit: int = 20,
) -> list[dict[str, Any]]:
    collection = db[collection_name]

    documents_cursor = collection.find(filter or {}, projection)

    if sort:
        documents_cursor = documents_cursor.sort(sort)

    if limit is not None:
        documents_cursor = documents_cursor.limit(limit)

    documents = list(documents_cursor)
    return documents


def find_one(
    db: Database,
    collection_name: str,
    filter: Optional[dict[str, Any]] = None,
    projection: Optional[dict[str, int]] = None,
) -> Optional[dict[str, Any]]:
    collection = db[collection_name]
    document = collection.find_one(filter or {}, projection)
    return document


def distinct_values(
    db: Database,
    collection_name: str,
    field: str,
    filter: Optional[dict[str, Any]] = None,
    limit: int = 100,
) -> list[Any]:
    collection = db[collection_name]
    values = collection.distinct(field, filter or {})
    # keep output small for learning
    return values[:limit]


def count(
    db: Database,
    collection_name: str,
    filter: Optional[dict[str, Any]] = None,
) -> int:
    collection = db[collection_name]
    return collection.count_documents(filter or {})