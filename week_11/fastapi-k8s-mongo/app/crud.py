from .database import db
from .models import Item

def create_item(item: Item):
    item_dict = item.dict()
    result = db.items.insert_one(item_dict)
    return str(result.inserted_id)

def get_items():
    return list(db.items.find({}, {"_id": 0}))
