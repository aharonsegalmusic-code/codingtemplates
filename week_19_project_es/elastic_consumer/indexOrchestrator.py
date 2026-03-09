"""
manages flow 
applies upsert by image_id
"""
# for local run 
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json

from shared.logger import get_logger
from shared.kafka_consumer import KafkaConsumerClient
from shared.kafka_publisher import KafkaPublisher 
from shared.es_connection import get_es_client

from indexerConfig import elasticConfig

class indexOrchestrator():
    def __init__(self,
                es_connection,
                kafka_consumer,
                consumer_topics,
                logger):
        self.es_connection = es_connection
        self.kafka_consumer = kafka_consumer
        self.consumer_topics = consumer_topics
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
    
    def poll_and_index(self, index: str):
        self.kafka_consumer.subscribe(self.consumer_topics)
        self.logger.info("index consumer started — listening to %s", self.consumer_topics)

        while True:
            image_data = self.get_image()
            image_id = image_data["image_id"]

            self.es_connection.update(
                index=index,
                id=image_id,
                body={"doc": image_data, "doc_as_upsert": True}
            )
            self.logger.info("upserted image_id=%s", image_id)

            

# ---- wiring ----
_logger = get_logger("index-service")
_config = elasticConfig()

orchestrator = indexOrchestrator(
    es_connection = get_es_client(),
    kafka_consumer = KafkaConsumerClient(
        bootstrap_servers = _config.bootstrap_servers,
        group_id = _config.indexer_group,
        logger = _logger
    ),
    consumer_topics = _config.kafka_topics_raw_clean,
    logger = _logger
)