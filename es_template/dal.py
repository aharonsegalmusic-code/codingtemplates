# dal.py  (Data Access Layer)
# ─────────────────────────────────────────────────────────────
# Responsibility: sits BETWEEN the routes and the raw ES queries.
# Routes call DAL methods; DAL calls PizzaQueries methods.
#
# Why a DAL?
#   Separation of concerns:
#     routes  → HTTP request/response shape
#     DAL     → business logic, data transformation
#     queries → raw ES DSL
#
#   If you swap ES for Postgres tomorrow you only rewrite the DAL
#   and queries — routes stay the same.
# ─────────────────────────────────────────────────────────────

from app.queries import pizza_queries


class PizzaDAL:
    """Business-logic layer for pizza order data."""

    # ── Simple pass-throughs ─────────────────────────────────
    # For now these just delegate, but you could add caching,
    # logging, or data transformation here later.

    def get_all_orders(self, size: int = 20) -> list[dict]:
        return pizza_queries.get_all(size=size)

    def search_by_instructions(self, text: str) -> list[dict]:
        return pizza_queries.search_instructions(text)

    def get_orders_by_pizza_type(self, pizza_type: str) -> list[dict]:
        return pizza_queries.get_by_pizza_type(pizza_type)

    def get_orders_by_delivery(self, is_delivery: bool) -> list[dict]:
        return pizza_queries.get_by_delivery(is_delivery)

    def get_orders_by_quantity_range(
        self, min_qty: int, max_qty: int
    ) -> list[dict]:
        return pizza_queries.get_by_quantity_range(min_qty, max_qty)

    def get_delivery_orders_by_type(self, pizza_type: str) -> list[dict]:
        return pizza_queries.get_delivery_orders_by_type(pizza_type)

    def fuzzy_search_type(self, pizza_type: str) -> list[dict]:
        return pizza_queries.fuzzy_search_type(pizza_type)

    def multi_field_search(self, text: str) -> list[dict]:
        return pizza_queries.multi_field_search(text)

    def get_order_by_id(self, order_id: str) -> dict | None:
        return pizza_queries.get_by_order_id(order_id)

    def wildcard_pizza_type(self, pattern: str) -> list[dict]:
        return pizza_queries.wildcard_pizza_type(pattern)

    # ── Aggregation methods ───────────────────────────────────
    def count_by_pizza_type(self) -> list[dict]:
        """Returns [{"key": "Pepperoni", "doc_count": 3}, ...]"""
        return pizza_queries.agg_count_by_pizza_type()

    def total_quantity_by_pizza_type(self) -> list[dict]:
        """Returns [{"key": "Pepperoni", "doc_count": 3, "total_qty": {"value": 8}}, ...]"""
        return pizza_queries.agg_total_quantity_by_type()


# ── Singleton ────────────────────────────────────────────────
pizza_dal = PizzaDAL()
