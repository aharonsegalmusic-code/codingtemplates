from fastapi import FastAPI
from .crud import create_item, get_items
from .models import Item

app = FastAPI()

@app.post("/items")
def add_item(item: Item):
    return {"id": create_item(item)}

@app.get("/items")
def list_items():
    return get_items()
