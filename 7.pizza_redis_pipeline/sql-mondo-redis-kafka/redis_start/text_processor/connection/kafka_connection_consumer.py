from confluent_kafka import Consumer
from dotenv import dotenv_values


ENV = dotenv_values(".env.local")

KAFKA_BOOTSTRAP_SERVERS = ENV.get("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9092")
KAFKA_GROUP_ID_TEXT = ENV.get("KAFKA_GROUP_ID_TEXT", "pizza-text")


class KafkaConsumerClient:
    def __init__(self, bootstrap_servers: str, group_id: str):
        self.consumer = Consumer({
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest"
        })

    def subscribe(self, topic: str):
        self.consumer.subscribe([topic])

    def poll(self, timeout: float = 1.0):
        return self.consumer.poll(timeout)

    def close(self):
        self.consumer.close()

consumer = KafkaConsumerClient(KAFKA_BOOTSTRAP_SERVERS,KAFKA_GROUP_ID_TEXT)

