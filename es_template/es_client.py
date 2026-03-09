# es_client.py
# ─────────────────────────────────────────────────────────────
# Responsibility: create and expose a single Elasticsearch
# client instance.  All other modules import `es` from here.
#
# Why a singleton?
#   The ES client maintains a connection pool internally.
#   Creating multiple clients wastes connections and memory.
# ─────────────────────────────────────────────────────────────

from elasticsearch import Elasticsearch
from app.config import ES_HOST


class ElasticsearchClient:
    """
    Thin wrapper that holds the official `elasticsearch-py` client.

    elasticsearch-py docs:
      https://elasticsearch-py.readthedocs.io/en/stable/
    """

    def __init__(self, host: str):
        # Elasticsearch(hosts=[...]) accepts a list of host strings.
        # Each string can be a full URL:  "http://localhost:9200"
        # or just a hostname: "localhost" (defaults to port 9200, HTTP).
        self._client = Elasticsearch(hosts=[host])

    def get_client(self) -> Elasticsearch:
        """Return the raw elasticsearch-py client."""
        return self._client

    def ping(self) -> bool:
        """
        Quick health check.
        Returns True when ES responds, False on timeout/error.
        """
        return self._client.ping()


# ── Module-level singleton ───────────────────────────────────
# When any file does `from app.es_client import es`, Python runs
# this line ONCE (module cache).  Every subsequent import gets
# the same object — no second connection pool is created.
es = ElasticsearchClient(host=ES_HOST).get_client()
