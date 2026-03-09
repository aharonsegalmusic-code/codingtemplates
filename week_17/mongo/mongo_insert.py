import json
from pathlib import Path
from typing import Any


# === CHANGE THIS ONLY ===
# collection_name -> json file path
JSON_FILES = {
    "stores": "data\stores.json",
    "purchases": "data\purchases.json",
    "customers": "data\customers.json",
}


def _load_json(path: str) -> list[dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"JSON file not found: {p.resolve()}")

    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # allow either {..} or [{..},{..}]
    if isinstance(data, dict):
        return [data]

    if isinstance(data, list) and all(isinstance(x, dict) for x in data):
        return data

    raise ValueError(f"{path} must be a JSON object or a JSON array of objects")


def insert_json_file(db, collection_name: str, json_path: str) -> int:
    collection = db[collection_name]
    documents = _load_json(json_path)

    if not documents:
        return 0

    result = collection.insert_many(documents, ordered=False)
    return len(result.inserted_ids)


def insert_all_json_files(db) -> dict:
    """
    Inserts all JSON_FILES into their collections.
    Returns a small report.
    """
    report: dict[str, int] = {}

    for collection_name, json_path in JSON_FILES.items():
        inserted = insert_json_file(db, collection_name, json_path)
        report[collection_name] = inserted

    return report