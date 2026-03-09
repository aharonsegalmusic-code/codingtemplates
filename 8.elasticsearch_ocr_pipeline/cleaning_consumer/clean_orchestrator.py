"""
gets from kafka
passes to be processed 
publishes to kafka
"""

# for local run 
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json

from clean_config import CleanConfig
from shared.logger import get_logger
from shared.kafka_consumer import KafkaConsumerClient
from shared.kafka_publisher import KafkaPublisher 
from text_cleaner import textCleaner

class cleanOrchestrator():
    def __init__(self,
                kafka_consumer,
                kafka_publisher,
                cleaner,
                logger):
        self.kafka_consumer = kafka_consumer
        self.producer = kafka_publisher
        self.cleaner = cleaner
        self.logger = logger

    def get_image(self):
        while True:
            image_data_bin = self.kafka_consumer.poll(5)
            if image_data_bin is None:
                self.logger.info("no message, polling again...")
                continue

            if image_data_bin.error():
                self.logger.error("kafka error: %s", image_data_bin.error())
                continue

            value = image_data_bin.value()
            if not value:
                self.logger.warning("empty message received")
                continue

            image_data = json.loads(value)
            self.logger.info("image id pulled: %s", image_data["image_id"])

            return image_data

    def start_cleaning(self, topic: str):
        self.kafka_consumer.subscribe(topic)
        self.logger.info("cleaning consumer started")

        while True:
            image_data = self.get_image()

            clean_tokens = self.cleaner(image_data["raw_text"])

            event = {
                "image_id": image_data["image_id"],
                "clean_text": clean_tokens,
                "metadata": image_data.get("metadata", {}),
            }

            self.producer.publish(event)
            self.logger.info("published clean event for image_id=%s", image_data["image_id"])


# ---- wiring ----
_logger = get_logger("cleaning-service")
_config = CleanConfig()

orchestrator = cleanOrchestrator(
    kafka_consumer = KafkaConsumerClient(
        bootstrap_servers = _config.bootstrap_servers,
        group_id = _config.clean_group,
        logger = _logger
    ),
    kafka_publisher = KafkaPublisher(_config.bootstrap_servers, _config.kafka_topic_clean, _logger),
    cleaner = textCleaner,
    logger = _logger
)