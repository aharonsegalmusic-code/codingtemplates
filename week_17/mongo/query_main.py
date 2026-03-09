# query_main.py
"""
EX3 MongoDB Aggregation - Query functions

This file contains ONE function per task (Q1..Q15).
Each function:
- receives `db` (PyMongo Database)
- builds an aggregation pipeline
- returns JSON-safe Python data (ObjectId-safe) for FastAPI responses
"""

import json
from typing import Any, Dict, List, Optional

from bson import json_util
from pymongo.database import Database


def _jsonable(value: Any) -> Any:
    """Convert MongoDB types (ObjectId, datetime, etc.) into JSON-safe Python types."""
    return json.loads(json_util.dumps(value))


# ------------------------------------------------------------
# Q1: Selection
# ------------------------------------------------------------
def q1_customers_basic_fields(db: Database, limit: int = 0) -> List[Dict[str, Any]]:
    """
    Show first_name, last_name, and country for all customers, hiding _id.
    """
    pipeline = [
        {"$project": {"_id": 0, "first_name": 1, "last_name": 1, "country": 1}},
    ]
    if limit and limit > 0:
        pipeline.append({"$limit": int(limit)})

    documents = list(db["customers"].aggregate(pipeline))
    return _jsonable(documents)


# ------------------------------------------------------------
# Q2: Basic Filtering
# ------------------------------------------------------------
def q2_israel_over_40(db: Database, limit: int = 0) -> List[Dict[str, Any]]:
    """
    Find all customers from Israel who are older than 40.
    """
    pipeline = [
        {"$match": {"country": "Israel", "age": {"$gt": 40}}},
        {"$project": {"_id": 0, "customer_id": 1, "first_name": 1, "last_name": 1, "age": 1, "country": 1}},
    ]
    if limit and limit > 0:
        pipeline.append({"$limit": int(limit)})

    documents = list(db["customers"].aggregate(pipeline))
    return _jsonable(documents)


# ------------------------------------------------------------
# Q3: Count & Match
# ------------------------------------------------------------
def q3_count_shipped_purchases(db: Database) -> Dict[str, int]:
    """
    Calculate how many purchases have status == 'shipped'.
    Returns: {"shipped_count": <int>}
    """
    pipeline = [
        {"$match": {"status": "shipped"}},
        {"$count": "shipped_count"},
    ]
    documents = list(db["purchases"].aggregate(pipeline))
    shipped_count = documents[0]["shipped_count"] if documents else 0
    return {"shipped_count": int(shipped_count)}


# ------------------------------------------------------------
# Q4: Join (Lookup)
# ------------------------------------------------------------
def q4_purchases_with_buyer_first_name(db: Database, limit: int = 0) -> List[Dict[str, Any]]:
    """
    Join purchases with customers to show:
    - item
    - buyer first_name
    """
    pipeline = [
        {
            "$lookup": {
                "from": "customers",
                "localField": "customer_id",
                "foreignField": "customer_id",
                "as": "customer",
            }
        },
        {"$unwind": "$customer"},
        {"$project": {"_id": 0, "item": 1, "first_name": "$customer.first_name"}},
    ]
    if limit and limit > 0:
        pipeline.append({"$limit": int(limit)})

    documents = list(db["purchases"].aggregate(pipeline))
    return _jsonable(documents)


# ------------------------------------------------------------
# Q5: Filtered Join
# ------------------------------------------------------------
def q5_purchases_by_gold_members(db: Database, limit: int = 0) -> List[Dict[str, Any]]:
    """
    Find all purchases made by 'Gold' members.
    Show: item, amount, membership
    """
    pipeline = [
        {
            "$lookup": {
                "from": "customers",
                "localField": "customer_id",
                "foreignField": "customer_id",
                "as": "customer",
            }
        },
        {"$unwind": "$customer"},
        {"$match": {"customer.membership": "Gold"}},
        {"$project": {"_id": 0, "item": 1, "amount": 1, "membership": "$customer.membership"}},
    ]
    if limit and limit > 0:
        pipeline.append({"$limit": int(limit)})

    documents = list(db["purchases"].aggregate(pipeline))
    return _jsonable(documents)


# ------------------------------------------------------------
# Q6: Store Join
# ------------------------------------------------------------
def q6_purchases_with_store_name(db: Database, limit: int = 0) -> List[Dict[str, Any]]:
    """
    Join purchases with stores to show:
    - item
    - store_name where it was purchased
    """
    pipeline = [
        {
            "$lookup": {
                "from": "stores",
                "localField": "store_id",
                "foreignField": "store_id",
                "as": "store",
            }
        },
        {"$unwind": "$store"},
        {"$project": {"_id": 0, "item": 1, "store_name": "$store.store_name"}},
    ]
    if limit and limit > 0:
        pipeline.append({"$limit": int(limit)})

    documents = list(db["purchases"].aggregate(pipeline))
    return _jsonable(documents)


# ------------------------------------------------------------
# Q7: Triple Join
# ------------------------------------------------------------
def q7_purchases_with_customer_and_store(db: Database, limit: int = 0) -> List[Dict[str, Any]]:
    """
    Join purchases with BOTH customers and stores.
    Show: first_name, item, store city
    """
    pipeline = [
        {
            "$lookup": {
                "from": "customers",
                "localField": "customer_id",
                "foreignField": "customer_id",
                "as": "customer",
            }
        },
        {"$unwind": "$customer"},
        {
            "$lookup": {
                "from": "stores",
                "localField": "store_id",
                "foreignField": "store_id",
                "as": "store",
            }
        },
        {"$unwind": "$store"},
        {"$project": {"_id": 0, "first_name": "$customer.first_name", "item": 1, "store_city": "$store.city"}},
    ]
    if limit and limit > 0:
        pipeline.append({"$limit": int(limit)})

    documents = list(db["purchases"].aggregate(pipeline))
    return _jsonable(documents)


# ------------------------------------------------------------
# Q8: Grouping
# ------------------------------------------------------------
def q8_total_spent_per_country(db: Database, limit: int = 0) -> List[Dict[str, Any]]:
    """
    Calculate the total amount of money spent per country.
    (purchases -> lookup customers -> group by customer.country)
    """
    pipeline = [
        {
            "$lookup": {
                "from": "customers",
                "localField": "customer_id",
                "foreignField": "customer_id",
                "as": "customer",
            }
        },
        {"$unwind": "$customer"},
        {"$group": {"_id": "$customer.country", "total_spent": {"$sum": "$amount"}}},
        {"$project": {"_id": 0, "country": "$_id", "total_spent": 1}},
        {"$sort": {"total_spent": -1}},
    ]
    if limit and limit > 0:
        pipeline.append({"$limit": int(limit)})

    documents = list(db["purchases"].aggregate(pipeline))
    return _jsonable(documents)


# ------------------------------------------------------------
# Q9: Sorting & Limits
# ------------------------------------------------------------
def q9_top_3_expensive_with_manager(db: Database) -> List[Dict[str, Any]]:
    """
    Find the top 3 most expensive purchases.
    Show: item, amount, store manager name
    """
    pipeline = [
        {
            "$lookup": {
                "from": "stores",
                "localField": "store_id",
                "foreignField": "store_id",
                "as": "store",
            }
        },
        {"$unwind": "$store"},
        {"$sort": {"amount": -1}},
        {"$limit": 3},
        {"$project": {"_id": 0, "item": 1, "amount": 1, "store_manager": "$store.manager"}},
    ]
    documents = list(db["purchases"].aggregate(pipeline))
    return _jsonable(documents)


# ------------------------------------------------------------
# Q10: Average Calculation
# ------------------------------------------------------------
def q10_avg_purchase_by_membership(db: Database) -> List[Dict[str, Any]]:
    """
    Find the average purchase amount for each membership type.
    """
    pipeline = [
        {
            "$lookup": {
                "from": "customers",
                "localField": "customer_id",
                "foreignField": "customer_id",
                "as": "customer",
            }
        },
        {"$unwind": "$customer"},
        {"$group": {"_id": "$customer.membership", "avg_amount": {"$avg": "$amount"}}},
        {"$project": {"_id": 0, "membership": "$_id", "avg_amount": 1}},
        {"$sort": {"avg_amount": -1}},
    ]
    documents = list(db["purchases"].aggregate(pipeline))
    return _jsonable(documents)


# ------------------------------------------------------------
# Q11: Multi-condition Join
# ------------------------------------------------------------
def q11_tech_purchases_in_london_stores(db: Database, limit: int = 0) -> List[Dict[str, Any]]:
    """
    Find all purchases of 'Tech' items made in stores located in 'London'.
    Show: item, amount, store_name, store_city
    """
    pipeline = [
        {"$match": {"category": "Tech"}},
        {
            "$lookup": {
                "from": "stores",
                "localField": "store_id",
                "foreignField": "store_id",
                "as": "store",
            }
        },
        {"$unwind": "$store"},
        {"$match": {"store.city": "London"}},
        {"$project": {"_id": 0, "item": 1, "amount": 1, "store_name": "$store.store_name", "store_city": "$store.city"}},
    ]
    if limit and limit > 0:
        pipeline.append({"$limit": int(limit)})

    documents = list(db["purchases"].aggregate(pipeline))
    return _jsonable(documents)


# ------------------------------------------------------------
# Q12: Aggregated Match
# ------------------------------------------------------------
def q12_countries_total_over_5000(db: Database) -> List[Dict[str, Any]]:
    """
    Show countries that have total purchase amount exceeding 5000.
    Returns: [{"country": "...", "total_spent": ...}, ...]
    """
    pipeline = [
        {
            "$lookup": {
                "from": "customers",
                "localField": "customer_id",
                "foreignField": "customer_id",
                "as": "customer",
            }
        },
        {"$unwind": "$customer"},
        {"$group": {"_id": "$customer.country", "total_spent": {"$sum": "$amount"}}},
        {"$match": {"total_spent": {"$gt": 5000}}},
        {"$project": {"_id": 0, "country": "$_id", "total_spent": 1}},
        {"$sort": {"total_spent": -1}},
    ]
    documents = list(db["purchases"].aggregate(pipeline))
    return _jsonable(documents)


# ------------------------------------------------------------
# Q13: Data Transformation
# ------------------------------------------------------------
def q13_store_name_uppercase(db: Database, limit: int = 0) -> List[Dict[str, Any]]:
    """
    Show store_name in uppercase and the manager name for all stores.
    """
    pipeline = [
        {"$project": {"_id": 0, "store_name_upper": {"$toUpper": "$store_name"}, "manager": 1}},
    ]
    if limit and limit > 0:
        pipeline.append({"$limit": int(limit)})

    documents = list(db["stores"].aggregate(pipeline))
    return _jsonable(documents)


# ------------------------------------------------------------
# Q14: Customer Behavior
# ------------------------------------------------------------
def q14_count_unique_items_bought_by_canada(db: Database) -> Dict[str, int]:
    """
    Count how many unique items were bought by customers from Canada.
    Returns: {"unique_items_count": <int>}
    """
    pipeline = [
        {
            "$lookup": {
                "from": "customers",
                "localField": "customer_id",
                "foreignField": "customer_id",
                "as": "customer",
            }
        },
        {"$unwind": "$customer"},
        {"$match": {"customer.country": "Canada"}},
        {"$group": {"_id": None, "unique_items": {"$addToSet": "$item"}}},
        {"$project": {"_id": 0, "unique_items_count": {"$size": "$unique_items"}}},
    ]
    documents = list(db["purchases"].aggregate(pipeline))
    unique_items_count = documents[0]["unique_items_count"] if documents else 0
    return {"unique_items_count": int(unique_items_count)}


# ------------------------------------------------------------
# Q15: Complex Summary
# ------------------------------------------------------------
def q15_store_city_revenue_and_max_purchase(db: Database, limit: int = 0) -> List[Dict[str, Any]]:
    """
    For each store city:
    - total revenue (sum of amount)
    - max amount spent on a single purchase (max of amount)
    """
    pipeline = [
        {
            "$lookup": {
                "from": "stores",
                "localField": "store_id",
                "foreignField": "store_id",
                "as": "store",
            }
        },
        {"$unwind": "$store"},
        {"$group": {"_id": "$store.city", "total_revenue": {"$sum": "$amount"}, "max_purchase": {"$max": "$amount"}}},
        {"$project": {"_id": 0, "store_city": "$_id", "total_revenue": 1, "max_purchase": 1}},
        {"$sort": {"total_revenue": -1}},
    ]
    if limit and limit > 0:
        pipeline.append({"$limit": int(limit)})

    documents = list(db["purchases"].aggregate(pipeline))
    return _jsonable(documents)