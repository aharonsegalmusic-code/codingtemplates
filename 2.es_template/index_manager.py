# index_manager.py
# ─────────────────────────────────────────────────────────────
# Responsibility: create the ES index with a proper mapping and
# bulk-load the pizza orders JSON into it.
#
# KEY CONCEPTS YOU WILL SEE HERE:
#
#  Index   — like a database table.  Holds documents.
#
#  Mapping — schema for an index.  Tells ES the data type of
#            each field so it knows how to index & search it.
#            Without a mapping ES guesses (dynamic mapping) —
#            fine for prototypes, but explicit is better.
#
#  Shard   — ES splits an index into N shards for horizontal
#            scaling.  1 shard is fine for dev/learning.
#
#  Replica — a copy of a shard on another node for HA.
#            0 replicas is fine when you have one node (Docker).
#
#  Bulk API — instead of indexing one document per HTTP request,
#             the bulk API sends many in one request.  Much faster.
# ─────────────────────────────────────────────────────────────

import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk   # bulk helper from the official library

from app.config import ES_INDEX, DATA_FILE
from app.es_client import es


# ── Mapping definition ───────────────────────────────────────
# We define every field explicitly.
#
# Field type cheat-sheet:
#   keyword  → exact match, sorting, aggregations  (e.g. enum values)
#   text     → full-text search with analysis      (e.g. free-form sentences)
#   integer  → whole numbers
#   boolean  → true / false
#
# A field can have BOTH text and keyword via a "fields" sub-mapping.
# This lets you do full-text search AND exact/sort on the same field.

PIZZA_MAPPING = {
    "settings": {
        # How many primary shards this index has.
        # For local dev 1 is enough; in production you'd set this
        # based on data volume (can't be changed after index creation).
        "number_of_shards": 1,

        # How many replica shards per primary.
        # 0 = no replicas (fine for single-node).
        # ES will warn if replicas > 0 and there is only one node.
        "number_of_replicas": 0,
    },
    "mappings": {
        "properties": {
            # ── keyword: exact match only ──────────────────────
            "order_id": {"type": "keyword"},

            # ── text + keyword ────────────────────────────────
            # "text" subfield  → full-text search (tokenised, lowercased)
            # "keyword" subfield → exact match, aggregations, sorting
            "pizza_type": {
                "type": "text",
                "fields": {
                    "keyword": {"type": "keyword"}   # accessed as pizza_type.keyword
                }
            },
            "size": {
                "type": "text",
                "fields": {
                    "keyword": {"type": "keyword"}   # accessed as size.keyword
                }
            },

            # ── numeric ───────────────────────────────────────
            "quantity": {"type": "integer"},

            # ── boolean ───────────────────────────────────────
            "is_delivery": {"type": "boolean"},

            # ── long text ─────────────────────────────────────
            # Only "text" — we won't sort or aggregate on it.
            # ES will tokenise this field so words like "allergy"
            # can be found regardless of surrounding text.
            "special_instructions": {"type": "text"},
        }
    },
}


class IndexManager:
    """
    Creates the ES index and loads documents into it.
    """

    def __init__(self, client: Elasticsearch, index: str, data_file: str):
        self.client    = client
        self.index     = index
        self.data_file = data_file

    # ── Index creation ───────────────────────────────────────
    def create_index(self):
        """
        Create the index if it doesn't already exist.

        indices.exists() → True/False
        indices.create() → sends PUT /<index> with settings + mappings
        """
        if self.client.indices.exists(index=self.index):
            print(f"[IndexManager] Index '{self.index}' already exists — skipping creation.")
            return

        self.client.indices.create(index=self.index, body=PIZZA_MAPPING)
        print(f"[IndexManager] Index '{self.index}' created with mapping.")

    def delete_index(self):
        """
        Drop the index entirely.  Useful to reset during development.
        """
        if self.client.indices.exists(index=self.index):
            self.client.indices.delete(index=self.index)
            print(f"[IndexManager] Index '{self.index}' deleted.")

    # ── Bulk loading ─────────────────────────────────────────
    def load_data(self):
        """
        Read the JSON file and bulk-index every order.

        The `bulk` helper from elasticsearch-py expects an iterable of
        action dicts.  Each action dict needs at minimum:
          _index  → which index to write to
          _id     → the document ID (we use order_id so re-runs are idempotent)
          _source → the actual document body

        Idempotent = safe to run multiple times;
        if _id already exists, ES will overwrite (upsert).
        """
        with open(self.data_file, "r") as f:
            orders = json.load(f)

        # Generator expression — produces one action dict per order.
        # Using a generator avoids loading all actions into RAM at once.
        actions = (
            {
                "_index":  self.index,
                "_id":     order["order_id"],   # stable doc ID
                "_source": order,
            }
            for order in orders
        )

        # bulk() returns (success_count, errors_list)
        success, errors = bulk(self.client, actions)
        print(f"[IndexManager] Indexed {success} documents. Errors: {errors}")


# ── Convenience entry point ──────────────────────────────────
def setup_index():
    """Called once at startup to ensure index + data exist."""
    manager = IndexManager(
        client    = es,
        index     = ES_INDEX,
        data_file = DATA_FILE,
    )
    manager.create_index()
    manager.load_data()
