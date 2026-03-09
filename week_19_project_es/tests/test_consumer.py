from confluent_kafka import Consumer
from logging import Logger
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import time
from shared.logger import get_logger

class KafkaConsumerClient:
    def __init__(self, bootstrap_servers: str, group_id: str,logger: Logger):
        self.consumer = Consumer({
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest"
        })
        self.logger = logger

    def subscribe(self, topic: str):
        self.consumer.subscribe([topic])
        self.logger.info("subscribed to %s", topic)


    def poll(self, timeout: float = 1.0):
        self.logger.info("did poll")
        return self.consumer.poll(timeout)

    def close(self):
        self.logger.info("close consumer")
        self.consumer.close()

class CleanConfig:

    def __init__(self):
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.clean_group = os.getenv("KAFKA_GROUP_CLEAN", "cleaning_group")
        self.kafka_topic_raw = os.getenv("KAFKA_TOPIC_RAW", "RAW")
        self.kafka_topic_clean = os.getenv("KAFKA_TOPIC_CLEAN", "clean")

logger = get_logger("testing")
config = CleanConfig()
consumer = KafkaConsumerClient(config.bootstrap_servers,config.clean_group,logger)
consumer.subscribe(config.kafka_topic_raw)

found = 0
while True:
    image_data_bin = consumer.poll(5)
    if image_data_bin is None:
        print("consume attempt complete")
        continue

    if image_data_bin.error():
        logger.error("kafka error: %s", image_data_bin.error())
        continue

    value = image_data_bin.value()
    if not value:
        logger.warning("empty message received")
        continue

    image_data = json.loads(value)
    print(image_data)
    print("consume complete")