"""
shared/kafka_publisher.py
Generic Kafka publisher — reused by all services.
Constructor: bootstrap_servers, topic_name, logger
"""

from logging import Logger
import json

from confluent_kafka import Producer


class KafkaPublisher:

    def __init__(self, bootstrap_servers: str, topic_name: str, logger: Logger):
        self.producer = Producer({"bootstrap.servers": bootstrap_servers})
        self.topic_name = topic_name
        self.logger = logger
        self.logger.info("KafkaPublisher ready — topic: %s", topic_name)

    def publish(self, event: dict) -> None:
        image_id = event.get("image_id", "unknown")
        self.logger.info("Publishing event for image_id=%s to %s", image_id, self.topic_name)

        try:
            self.producer.produce(
                topic=self.topic_name,
                key=image_id,
                value=json.dumps(event).encode("utf-8"),
            )
            self.producer.flush()
            self.logger.info("Published image_id=%s", image_id)

        except Exception as e:
            self.logger.error("Failed to publish event: %s", e)
            raise
