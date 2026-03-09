"""
Enricher Service - Kosher & Ingredient Analysis

INPUT:
    - Kafka topic "cleaned-instructions" (consumes cleaned order data)
      fields: order_id, pizza_type, special_instructions (cleaned), cleaned_prep

OUTPUT:
    - analyzes pizza against closed lists (allergens, non-kosher, meat, dairy)
    - caches pizza_type metadata in Redis (TTL 5s) to avoid re-analysis
    - updates MongoDB with: is_meat, is_dairy, is_kosher, non_kosher,
      allergens, clean_special_instructions, cleaned_prep, insertion_time
    - if not kosher -> sets status to "BURNT"

FLOW:
    Kafka "cleaned-instructions" -> enricher -> Redis (cache check for pizza_type)
                                             -> analyze() if cache miss
                                             -> MongoDB (update analysis fields)
"""

from .connection.kafka_connection_consumer import consumer
from .connection.mongo_connection import mongo
from .connection.redis_connection import r
import json
from datetime import datetime, timezone

import os
from dotenv import dotenv_values
ENV = {**dotenv_values(".env.local"), **os.environ}
TOPIC_CLEAN_INST = ENV.get("TOPIC_CLEAN_INST", "cleaned-instructions")

collection = mongo.collection("pizza_orders")
consumer.subscribe(TOPIC_CLEAN_INST)

with open('data/pizza_analysis_lists.json', 'r') as file:
    pizza_analysis_lists = json.load(file)


def analyze(pizza_type, cleaned_prep, clean_special_instructions):
    """
    Analyze the pizza based on cleaned prep text and special instructions
    against the closed lists (allergens, non-kosher, meat, dairy).
    Returns a dict with analysis metadata.
    """
    # combine both cleaned texts for scanning
    combined_text = (cleaned_prep + " " + clean_special_instructions).upper()

    pizza = {
        "pizza_type": pizza_type,
        "hit": False,
        "non_kosher": False,
        "is_meat": False,
        "is_dairy": True,   # default: every pizza is dairy
        "is_kosher": True,
        "allergens": False
    }

    # step 1 -> check forbidden_non_kosher
    if any(item.upper() in combined_text for item in pizza_analysis_lists["forbidden_non_kosher"]):
        pizza["non_kosher"] = True
        pizza["hit"] = True
        pizza["is_kosher"] = False

    # step 2 -> check common_allergens
    if any(item.upper() in combined_text for item in pizza_analysis_lists["common_allergens"]):
        pizza["allergens"] = True

    # step 3 -> check dairy_ingredients
    if any(item.upper() in combined_text for item in pizza_analysis_lists["dairy_ingredients"]):
        pizza["hit"] = True

    # step 4 -> check meat_ingredients
    if any(item.upper() in combined_text for item in pizza_analysis_lists["meat_ingredients"]):
        pizza["hit"] = True
        pizza["is_meat"] = True

    # kosher rule: meat + dairy together = not kosher
    if pizza["is_dairy"] and pizza["is_meat"]:
        pizza["is_kosher"] = False

    return pizza


def enricher_consumer():
    """
    listens to kafka cleaned-instructions topic
    for each order:
        1. checks redis cache for pizza_type metadata (TTL 5s)
        2. if cache miss -> runs analyze() and caches result
        3. updates mongo with analysis metadata + insertion_time
        4. if not kosher -> sets status to BURNT
    """
    print("enricher running...")
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"enricher_consumer error: {msg.error()}")
                continue

            order = json.loads(msg.value())
            order_id = order["order_id"]
            pizza_type = order["pizza_type"]
            clean_special_instructions = order.get("special_instructions", "")
            cleaned_prep = order.get("cleaned_prep", "")

            # check redis cache for pizza_type metadata
            redis_cached = r.get(pizza_type)

            if redis_cached:
                # cache hit - use cached analysis
                pizza = json.loads(redis_cached)
                print(f"[CACHE HIT] {pizza_type}")
            else:
                # cache miss - run full analysis
                pizza = analyze(pizza_type, cleaned_prep, clean_special_instructions)
                # store in redis with TTL 5 seconds
                r.set(pizza_type, json.dumps(pizza), ex=5)
                print(f"[CACHE MISS] {pizza_type} -> analyzed and cached")

            # build the update for mongo
            update_fields = {
                "is_meat": pizza["is_meat"],
                "is_dairy": pizza["is_dairy"],
                "is_kosher": pizza["is_kosher"],
                "non_kosher": pizza["non_kosher"],
                "allergens": pizza["allergens"],
                "clean_special_instructions": clean_special_instructions,
                "cleaned_prep": cleaned_prep,
                "insertion_time": datetime.now(timezone.utc).isoformat()
            }

            # if not kosher -> BURNT
            if not pizza["is_kosher"]:
                update_fields["status"] = "BURNT"
                print(f"[BURNT] order_id={order_id} pizza_type={pizza_type}")

            collection.update_one(
                {"order_id": order_id},
                {"$set": update_fields}
            )

            print(f"[ENRICHED] order_id={order_id} pizza_type={pizza_type} is_kosher={pizza['is_kosher']}")

    finally:
        consumer.close()


enricher_consumer()

# python -m enricher.enricher_consumer
