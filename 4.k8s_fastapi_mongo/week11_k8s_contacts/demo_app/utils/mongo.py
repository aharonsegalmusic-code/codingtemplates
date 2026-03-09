from bson import ObjectId

def to_objectId(id: str) -> ObjectId:
    return ObjectId(id)