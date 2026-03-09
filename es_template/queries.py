# queries.py
# ─────────────────────────────────────────────────────────────
# Responsibility: every Elasticsearch query the app needs.
# Each method returns a plain Python list of dicts (the hits).
#
# QUERY ANATOMY (Elasticsearch Query DSL):
#
#   {
#     "query": { ... },      ← what to match / filter
#     "size":  N,            ← max documents to return (default 10)
#     "from":  N,            ← pagination offset
#     "sort":  [ ... ],      ← how to order results
#     "aggs":  { ... },      ← aggregations (GROUP BY equivalent)
#     "_source": [...]       ← which fields to return
#   }
#
# QUERY TYPES YOU WILL SEE HERE:
#
#   match        → full-text search on a "text" field
#                  ES analyses the input (lowercase, tokenise) before
#                  comparing it to the analysed index.
#
#   match_all    → return every document (like SELECT * with no WHERE)
#
#   term         → exact match on a "keyword" field
#                  No analysis — the value must match byte-for-byte.
#
#   terms        → like term but accepts a list (SQL: WHERE x IN (...))
#
#   range        → numeric / date comparison (>, <, >=, <=)
#
#   bool         → boolean combinator:
#                    must    → AND  (must match, affects score)
#                    filter  → AND  (must match, does NOT affect score → faster)
#                    should  → OR   (at least one should match)
#                    must_not→ NOT
#
#   multi_match  → match across several fields at once
#
#   wildcard     → glob-style pattern on a keyword field  (*pep*)
#                  Slow on large indexes — avoid in production.
#
#   fuzzy        → approximate match (handles typos)
#
#   aggregations → analytics / GROUP BY
#                    terms agg  → count docs per unique value
#                    sum agg    → add up a numeric field
# ─────────────────────────────────────────────────────────────

from elasticsearch import Elasticsearch
from app.config import ES_INDEX
from app.es_client import es


def _hits(response: dict) -> list[dict]:
    """
    ES always returns results inside response["hits"]["hits"].
    Each hit has:
      _index, _id, _score, _source (the actual document)
    We flatten to just the _source for simplicity.
    """
    return [hit["_source"] for hit in response["hits"]["hits"]]


class PizzaQueries:
    """All search queries for the pizza_orders index."""

    def __init__(self, client: Elasticsearch, index: str):
        self.client = client
        self.index  = index

    # ── 1. Get all orders ────────────────────────────────────
    def get_all(self, size: int = 20) -> list[dict]:
        """
        match_all: returns every document.
        `size` controls the page size (ES default is 10).

        DSL:
          { "query": { "match_all": {} } }
        """
        response = self.client.search(
            index = self.index,
            body  = {
                "query": {"match_all": {}},
                "size":  size,
            },
        )
        return _hits(response)

    # ── 2. Full-text search on special_instructions ──────────
    def search_instructions(self, text: str) -> list[dict]:
        """
        match query on a `text` field.

        ES will:
          1. Analyse the search text  (lowercase, split on spaces)
          2. Analyse the indexed field (same pipeline)
          3. Return docs where any token matches

        Example: search_instructions("allergy") finds "PEANUT allergy!!!"
        because both are lowercased to "allergy" at index+query time.

        DSL:
          { "query": { "match": { "special_instructions": "allergy" } } }
        """
        response = self.client.search(
            index = self.index,
            body  = {
                "query": {
                    "match": {
                        "special_instructions": text
                    }
                }
            },
        )
        return _hits(response)

    # ── 3. Exact match on pizza type ─────────────────────────
    def get_by_pizza_type(self, pizza_type: str) -> list[dict]:
        """
        term query on pizza_type.keyword (exact, case-sensitive).

        Why .keyword?
          `pizza_type` is mapped as text+keyword.
          The `text` subfield is analysed (lowercased, tokenised).
          The `keyword` subfield stores the ORIGINAL value — exact.

        Use term+keyword when you know the precise value:
          "Pepperoni" != "pepperoni" on a keyword field.

        DSL:
          { "query": { "term": { "pizza_type.keyword": "Pepperoni" } } }
        """
        response = self.client.search(
            index = self.index,
            body  = {
                "query": {
                    "term": {
                        "pizza_type.keyword": pizza_type
                    }
                }
            },
        )
        return _hits(response)

    # ── 4. Filter by delivery flag ────────────────────────────
    def get_by_delivery(self, is_delivery: bool) -> list[dict]:
        """
        term query on a boolean field.
        filter clause → no score calculation → faster.

        bool/filter is preferred over bool/must when you don't care
        about relevance ranking, only inclusion/exclusion.

        DSL:
          {
            "query": {
              "bool": {
                "filter": [ { "term": { "is_delivery": true } } ]
              }
            }
          }
        """
        response = self.client.search(
            index = self.index,
            body  = {
                "query": {
                    "bool": {
                        "filter": [
                            {"term": {"is_delivery": is_delivery}}
                        ]
                    }
                }
            },
        )
        return _hits(response)

    # ── 5. Filter by quantity range ───────────────────────────
    def get_by_quantity_range(self, min_qty: int, max_qty: int) -> list[dict]:
        """
        range query.  Operators: gte (≥), lte (≤), gt (>), lt (<).

        DSL:
          {
            "query": {
              "range": { "quantity": { "gte": 2, "lte": 5 } }
            }
          }
        """
        response = self.client.search(
            index = self.index,
            body  = {
                "query": {
                    "range": {
                        "quantity": {
                            "gte": min_qty,
                            "lte": max_qty,
                        }
                    }
                }
            },
        )
        return _hits(response)

    # ── 6. Combined filter: delivery + pizza type ─────────────
    def get_delivery_orders_by_type(self, pizza_type: str) -> list[dict]:
        """
        bool query combining multiple conditions.

        must   → scored AND  (affects relevance rank)
        filter → non-scored AND (faster, good for exact conditions)

        Here we put both in `filter` because ranking doesn't matter.

        DSL:
          {
            "query": {
              "bool": {
                "filter": [
                  { "term": { "is_delivery": true } },
                  { "term": { "pizza_type.keyword": "Pepperoni" } }
                ]
              }
            }
          }
        """
        response = self.client.search(
            index = self.index,
            body  = {
                "query": {
                    "bool": {
                        "filter": [
                            {"term": {"is_delivery": True}},
                            {"term": {"pizza_type.keyword": pizza_type}},
                        ]
                    }
                }
            },
        )
        return _hits(response)

    # ── 7. Fuzzy search (typo-tolerant) ──────────────────────
    def fuzzy_search_type(self, pizza_type: str) -> list[dict]:
        """
        fuzzy query: finds results within an edit distance.
        fuzziness "AUTO":
          0-2 char terms  → exact
          3-5 char terms  → 1 edit
          6+ char terms   → 2 edits

        Example: "Peperoni" (typo) still finds "Pepperoni".

        fuzzy works on `text` fields; ES analyses the query first,
        then applies fuzzy matching on the tokens.

        DSL:
          {
            "query": {
              "fuzzy": {
                "pizza_type": { "value": "Peperoni", "fuzziness": "AUTO" }
              }
            }
          }
        """
        response = self.client.search(
            index = self.index,
            body  = {
                "query": {
                    "fuzzy": {
                        "pizza_type": {
                            "value":     pizza_type,
                            "fuzziness": "AUTO",
                        }
                    }
                }
            },
        )
        return _hits(response)

    # ── 8. Multi-field full-text search ──────────────────────
    def multi_field_search(self, text: str) -> list[dict]:
        """
        multi_match: run the same search across multiple fields.

        type "best_fields" (default): score from the field with
        the highest single match score wins.

        DSL:
          {
            "query": {
              "multi_match": {
                "query":  "allergy",
                "fields": ["special_instructions", "pizza_type"]
              }
            }
          }
        """
        response = self.client.search(
            index = self.index,
            body  = {
                "query": {
                    "multi_match": {
                        "query":  text,
                        "fields": ["special_instructions", "pizza_type"],
                    }
                }
            },
        )
        return _hits(response)

    # ── 9. Aggregation: order count by pizza type ─────────────
    def agg_count_by_pizza_type(self) -> dict:
        """
        Terms aggregation = GROUP BY pizza_type + COUNT(*).

        `size: 0` in the top-level query means: don't return
        actual documents, only the aggregation results.
        This is a performance optimisation.

        Agg result structure:
          response["aggregations"]["by_type"]["buckets"]
          → [ {"key": "Pepperoni", "doc_count": 3}, ... ]

        DSL:
          {
            "size": 0,
            "aggs": {
              "by_type": {
                "terms": { "field": "pizza_type.keyword", "size": 20 }
              }
            }
          }
        """
        response = self.client.search(
            index = self.index,
            body  = {
                "size": 0,    # no hits, only aggregations
                "aggs": {
                    "by_type": {                     # arbitrary bucket name
                        "terms": {
                            "field": "pizza_type.keyword",
                            "size":  20,             # max unique buckets
                        }
                    }
                },
            },
        )
        # Return the buckets directly for easy JSON serialisation
        return response["aggregations"]["by_type"]["buckets"]

    # ── 10. Aggregation: total quantity by pizza type ─────────
    def agg_total_quantity_by_type(self) -> dict:
        """
        Sum aggregation inside a terms aggregation.
        → For each pizza type, sum all quantities ordered.

        DSL:
          {
            "size": 0,
            "aggs": {
              "by_type": {
                "terms": { "field": "pizza_type.keyword" },
                "aggs": {
                  "total_qty": { "sum": { "field": "quantity" } }
                }
              }
            }
          }
        """
        response = self.client.search(
            index = self.index,
            body  = {
                "size": 0,
                "aggs": {
                    "by_type": {
                        "terms": {"field": "pizza_type.keyword", "size": 20},
                        "aggs": {
                            "total_qty": {
                                "sum": {"field": "quantity"}
                            }
                        },
                    }
                },
            },
        )
        return response["aggregations"]["by_type"]["buckets"]

    # ── 11. Wildcard search on pizza type ─────────────────────
    def wildcard_pizza_type(self, pattern: str) -> list[dict]:
        """
        Wildcard on a keyword field.
        * = any sequence of characters   (like SQL %)
        ? = any single character         (like SQL _)

        Example: pattern="*Chicken*" finds "Thai Chicken", "BBQ Chicken"

        ⚠ Wildcards leading with * are slow on large datasets
           because ES can't use the index efficiently.

        DSL:
          { "query": { "wildcard": { "pizza_type.keyword": "*Chicken*" } } }
        """
        response = self.client.search(
            index = self.index,
            body  = {
                "query": {
                    "wildcard": {
                        "pizza_type.keyword": pattern
                    }
                }
            },
        )
        return _hits(response)

    # ── 12. Get a single document by order_id ─────────────────
    def get_by_order_id(self, order_id: str) -> dict | None:
        """
        Fetch one document by its document ID (not a search query).

        client.get() bypasses the search engine entirely and reads
        directly from the shard — O(1), always fast.

        Returns the _source dict, or None if not found.
        """
        try:
            response = self.client.get(index=self.index, id=order_id)
            return response["_source"]
        except Exception:
            return None


# ── Module-level singleton (mirrors es_client pattern) ───────
pizza_queries = PizzaQueries(client=es, index=ES_INDEX)
