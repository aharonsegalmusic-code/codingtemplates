# routes_query_main.py
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from pymongo.database import Database

import query_main as qm

router = APIRouter()


def get_db(request: Request) -> Database:
    return request.app.state.mongo.db


"""
DB = Annotated[Database, Depends(get_db)]
When a route parameter is typed as `DB`, FastAPI calls `get_db()` and injects the Database automatically.
"""
DB = Annotated[Database, Depends(get_db)]


# ----------------------------
# EX3 Endpoints (Q1..Q15)
# ----------------------------

@router.get("/q1", name="ex3_q1", operation_id="ex3_q1")
def ex3_q1(db: DB, limit: int = 0):
    return {"documents": qm.q1_customers_basic_fields(db, limit=limit)}


@router.get("/q2", name="ex3_q2", operation_id="ex3_q2")
def ex3_q2(db: DB, limit: int = 0):
    return {"documents": qm.q2_israel_over_40(db, limit=limit)}


@router.get("/q3", name="ex3_q3", operation_id="ex3_q3")
def ex3_q3(db: DB):
    return qm.q3_count_shipped_purchases(db)


@router.get("/q4", name="ex3_q4", operation_id="ex3_q4")
def ex3_q4(db: DB, limit: int = 0):
    return {"documents": qm.q4_purchases_with_buyer_first_name(db, limit=limit)}


@router.get("/q5", name="ex3_q5", operation_id="ex3_q5")
def ex3_q5(db: DB, limit: int = 0):
    return {"documents": qm.q5_purchases_by_gold_members(db, limit=limit)}


@router.get("/q6", name="ex3_q6", operation_id="ex3_q6")
def ex3_q6(db: DB, limit: int = 0):
    return {"documents": qm.q6_purchases_with_store_name(db, limit=limit)}


@router.get("/q7", name="ex3_q7", operation_id="ex3_q7")
def ex3_q7(db: DB, limit: int = 0):
    return {"documents": qm.q7_purchases_with_customer_and_store(db, limit=limit)}


@router.get("/q8", name="ex3_q8", operation_id="ex3_q8")
def ex3_q8(db: DB, limit: int = 0):
    return {"documents": qm.q8_total_spent_per_country(db, limit=limit)}


@router.get("/q9", name="ex3_q9", operation_id="ex3_q9")
def ex3_q9(db: DB):
    return {"documents": qm.q9_top_3_expensive_with_manager(db)}


@router.get("/q10", name="ex3_q10", operation_id="ex3_q10")
def ex3_q10(db: DB):
    return {"documents": qm.q10_avg_purchase_by_membership(db)}


@router.get("/q11", name="ex3_q11", operation_id="ex3_q11")
def ex3_q11(db: DB, limit: int = 0):
    return {"documents": qm.q11_tech_purchases_in_london_stores(db, limit=limit)}


@router.get("/q12", name="ex3_q12", operation_id="ex3_q12")
def ex3_q12(db: DB):
    return {"documents": qm.q12_countries_total_over_5000(db)}


@router.get("/q13", name="ex3_q13", operation_id="ex3_q13")
def ex3_q13(db: DB, limit: int = 0):
    return {"documents": qm.q13_store_name_uppercase(db, limit=limit)}


@router.get("/q14", name="ex3_q14", operation_id="ex3_q14")
def ex3_q14(db: DB):
    return qm.q14_count_unique_items_bought_by_canada(db)


@router.get("/q15", name="ex3_q15", operation_id="ex3_q15")
def ex3_q15(db: DB, limit: int = 0):
    return {"documents": qm.q15_store_city_revenue_and_max_purchase(db, limit=limit)}