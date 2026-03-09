import os
import time
from typing import Optional

from confluent_kafka import KafkaError, Producer
from confluent_kafka.admin import AdminClient, NewTopic


BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")

producer = Producer(
    {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        # good defaults for dev; safe even if you don't use keys
        "client.id": "producer-api",
    }
)


def ensure_topic_exists(
    topic: str,
    partitions: int = 1,
    replication_factor: int = 1,
    retries: int = 30,
    sleep_seconds: float = 2.0,
    timeout_seconds: float = 10.0,
) -> None:
    """
    Long-term fix:
    - Make sure the topic exists before consumers subscribe / producer produces.
    - Idempotent: safe to call multiple times.
    - Retries to handle Kafka not ready yet.
    """
    admin = AdminClient({"bootstrap.servers": BOOTSTRAP_SERVERS})
    last_err: Optional[Exception] = None

    for _ in range(retries):
        try:
            md = admin.list_topics(timeout=timeout_seconds)

            if topic in md.topics and md.topics[topic].error is None:
                return

            futures = admin.create_topics(
                [NewTopic(topic, num_partitions=partitions, replication_factor=replication_factor)]
            )
            futures[topic].result(timeout=timeout_seconds)
            return

        except Exception as e:
            last_err = e

            # Ignore "already exists" errors (different versions format this differently)
            msg = str(e)
            if "TOPIC_ALREADY_EXISTS" in msg or "Topic already exists" in msg:
                return

            # If Kafka isn't ready yet / connection issues, just retry
            time.sleep(sleep_seconds)

    raise RuntimeError(f"Kafka topic '{topic}' not ready / could not be created. Last error: {last_err}")