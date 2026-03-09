from .connection.kafka_connection_consumer import consumer
from .connection.mongo_connection import mongo
from .connection.redis_connection import r
import json


from dotenv import dotenv_values
ENV = dotenv_values(".env.local")
TOPIC_CLEAN_INST = ENV.get("TOPIC_CLEAN_INST", "cleaned-instructions")

collection = mongo.collection("pizza_orders")
consumer.subscribe(TOPIC_CLEAN_INST)

with open('data\pizza_analysis_lists.json', 'r') as file:
    pizza_analysis_lists = json.load(file)

# SET based on criteria to BURNT
def analyze(pizza_type):
    pizza = {"pizza_type" : pizza_type,
            "hit" : False,
            "non_kosher" : False,
            "is_meat" : False,
            "is_dairy" : True,
            "is_kosher" : True,
            "allergens" : False
            }

    # step 1 -> NOT KOSHER
    if any(pizza_type in pizza_analysis_lists[key] for key in ["forbidden_non_kosher"]):
        pizza["non_kosher"] = True
        pizza["hit"] = True
        pizza["is_kosher"] = False

    # step 1 
    if any(pizza_type in pizza_analysis_lists[key] for key in ["common_allergens"]):
        pizza["allergens"] = True

    # step 1 
    if any(pizza_type in pizza_analysis_lists[key] for key in ["dairy_ingredients"]):
        pizza["hit"] = True

    # step 1 
    if any(pizza_type in pizza_analysis_lists[key] for key in ["meat_ingredients"]):
        pizza["hit"] = True
        pizza["is_meat"] = True

    if pizza["is_dairy"] and pizza["is_meat"]:
        pizza["is_kosher"] = False  

    return pizza
    

def enricher_consumer():
    """
    listens to kafka 
    for order_id
    checks if kosher in 2 ways
        1: checks in redis 
            if not 
        2: runs analyze()
            gets the pizza is kosher params
    returns dict 
        key: pizza_type
        value: kosher params dict
    """

    print("running")
    try:
        while True:
            order = consumer.poll(1.0) 
            if order is None: continue
            if order.error():
                print(f"enricher_consumer error: {order.error()}")
                continue

            order = json.loads(order.value())
            order_id = order["order_id"]

            #start analysis
            pizza_type = order["pizza_type"]
            # check if in redis
            redis_kosher = r.get(pizza_type)
            if not redis_kosher:
                pizza = analyze(order_id)
                redis_order= r.set(pizza_type, pizza)
                
            else:
                # update in mongo as BURNT
                collection.update_one(
                {"order_id": order_id},
                {"$set": {"status": "Burnt"}},
                )           


    finally:
        consumer.close()


enricher_consumer()

# python -m enricher_consumer.enricher_consumer_worker