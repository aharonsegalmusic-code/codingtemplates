"""
es_connection.py
Shared Elasticsearch connection factory.

Usage:
    from es_connection import get_es_client

    es = get_es_client(logger=logger)
    es.index(index="images", id="123", document={...})
"""

import os
from logging import Logger
from elasticsearch import Elasticsearch


def get_es_client(
    url: str | None = None,
    logger: Logger | None = None,
) -> Elasticsearch:
    """
    Create and verify an Elasticsearch client.

    Args:
        url:    Elasticsearch URL. Falls back to ELASTICSEARCH_URL env var.
        logger: Optional logger for connection status.

    Returns:
        Connected Elasticsearch client.

    Raises:
        ConnectionError: If Elasticsearch is unreachable.
    """
    url = url or os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")

    es = Elasticsearch(url)

    # verify connection
    if not es.ping():
        msg = f"Elasticsearch is unreachable at {url}"
        if logger:
            logger.error(msg)
        raise ConnectionError(msg)

    if logger:
        info = es.info()
        logger.info(
            "Connected to Elasticsearch %s at %s (cluster: %s)",
            info["version"]["number"],
            url,
            info["cluster_name"],
        )

    return es
