# routes.py
# ─────────────────────────────────────────────────────────────
# Responsibility: HTTP layer only.
# Each route:
#   1. Reads input from path params / query params / body
#   2. Calls the DAL
#   3. Returns the result (FastAPI auto-serialises dicts to JSON)
#
# Router is created here and registered in main.py.
# ─────────────────────────────────────────────────────────────

from fastapi import APIRouter, HTTPException, Query
from app.dal import pizza_dal

router = APIRouter(prefix="/orders", tags=["Pizza Orders"])


# ── GET /orders ───────────────────────────────────────────────
@router.get("/")
def get_all_orders(size: int = Query(default=20, ge=1, le=100)):
    """
    Return all pizza orders.
    Query param `size` controls max results (1-100).
    """
    return pizza_dal.get_all_orders(size=size)


# ── GET /orders/{order_id} ────────────────────────────────────
@router.get("/{order_id}")
def get_order_by_id(order_id: str):
    """
    Fetch a single order by its ID (e.g. order_1001).
    Uses ES .get() — not a search, direct document lookup.
    """
    order = pizza_dal.get_order_by_id(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found.")
    return order


# ── GET /orders/search/instructions ──────────────────────────
@router.get("/search/instructions")
def search_instructions(q: str = Query(..., description="Text to search in special instructions")):
    """
    Full-text search in the `special_instructions` field.
    Example: /orders/search/instructions?q=allergy
    """
    return pizza_dal.search_by_instructions(q)


# ── GET /orders/search/multi ──────────────────────────────────
@router.get("/search/multi")
def multi_search(q: str = Query(..., description="Search across pizza_type and special_instructions")):
    """
    Multi-field search: scans both `pizza_type` and `special_instructions`.
    """
    return pizza_dal.multi_field_search(q)


# ── GET /orders/filter/type ───────────────────────────────────
@router.get("/filter/type")
def filter_by_type(pizza_type: str = Query(..., description="Exact pizza type e.g. Pepperoni")):
    """
    Exact match on pizza_type.keyword.
    Case-sensitive — 'pepperoni' won't match 'Pepperoni'.
    """
    return pizza_dal.get_orders_by_pizza_type(pizza_type)


# ── GET /orders/filter/delivery ───────────────────────────────
@router.get("/filter/delivery")
def filter_by_delivery(is_delivery: bool = Query(...)):
    """
    Filter by delivery flag.
    Example: /orders/filter/delivery?is_delivery=true
    """
    return pizza_dal.get_orders_by_delivery(is_delivery)


# ── GET /orders/filter/quantity ───────────────────────────────
@router.get("/filter/quantity")
def filter_by_quantity(
    min_qty: int = Query(default=1, ge=1),
    max_qty: int = Query(default=10, le=100),
):
    """
    Range filter on quantity.
    Example: /orders/filter/quantity?min_qty=2&max_qty=5
    """
    return pizza_dal.get_orders_by_quantity_range(min_qty, max_qty)


# ── GET /orders/filter/delivery-by-type ───────────────────────
@router.get("/filter/delivery-by-type")
def delivery_orders_by_type(pizza_type: str = Query(...)):
    """
    Combined filter: delivery=True AND pizza_type matches exactly.
    """
    return pizza_dal.get_delivery_orders_by_type(pizza_type)


# ── GET /orders/search/fuzzy ──────────────────────────────────
@router.get("/search/fuzzy")
def fuzzy_type(q: str = Query(..., description="Approximate pizza type (typos ok)")):
    """
    Fuzzy search on pizza_type — tolerates typos.
    Example: /orders/search/fuzzy?q=Peperoni  → matches Pepperoni
    """
    return pizza_dal.fuzzy_search_type(q)


# ── GET /orders/search/wildcard ───────────────────────────────
@router.get("/search/wildcard")
def wildcard_type(pattern: str = Query(..., description="Wildcard pattern e.g. *Chicken*")):
    """
    Wildcard search on pizza_type.keyword.
    Use * for any chars, ? for one char.
    """
    return pizza_dal.wildcard_pizza_type(pattern)


# ── GET /orders/agg/count-by-type ─────────────────────────────
@router.get("/agg/count-by-type")
def agg_count_by_type():
    """
    Aggregation: number of orders per pizza type.
    Returns buckets: [{"key": "Pepperoni", "doc_count": 3}, ...]
    """
    return pizza_dal.count_by_pizza_type()


# ── GET /orders/agg/quantity-by-type ──────────────────────────
@router.get("/agg/quantity-by-type")
def agg_quantity_by_type():
    """
    Aggregation: total pizzas ordered per type.
    Returns buckets with nested sum value.
    """
    return pizza_dal.total_quantity_by_pizza_type()
