from confluent_kafka import Consumer
from logging import Logger

class KafkaConsumerClient:
    def __init__(self, bootstrap_servers: str, group_id: str,logger: Logger):
        self.consumer = Consumer({
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest"
        })
        self.logger = logger

    def subscribe(self, topics):
        if isinstance(topics, str):
            topics = [topics]
        self.consumer.subscribe(topics)
        self.logger.info("subscribed to %s", topics)


    def poll(self, timeout: float = 1.0):
        self.logger.info("did poll")
        return self.consumer.poll(timeout)

    def close(self):
        self.logger.info("close consumer")
        self.consumer.close()

# consumer = KafkaConsumerClient(KAFKA_BOOTSTRAP_SERVERS,KAFKA_GROUP_ID_TEXT)

