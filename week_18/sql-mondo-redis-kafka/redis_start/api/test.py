import json
from pydantic import BaseModel

# Open the file in read mode ('r') using a context manager
with open('data\pizza_orders.json', 'r') as file:
    # Parse the JSON data from the file object into a Python dictionary/list
    data = json.load(file)
    
class Order(BaseModel):
    order_id: str
    size: str
    quantity: int 
    is_delivery: bool = False
    special_instructions: str = ""
    status: str = "PREPARING"

for order in data:
    current = Order(**order)
    print("==========")
    print(current)
    break
