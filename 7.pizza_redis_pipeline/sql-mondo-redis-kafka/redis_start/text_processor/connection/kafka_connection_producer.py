from confluent_kafka import Producer
import json
from typing import Callable
from dotenv import dotenv_values


ENV = dotenv_values(".env.local")

KAFKA_BOOTSTRAP_SERVERS = ENV.get("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9092")


class KafkaProducerClient:
    def __init__(self, bootstrap_servers: str):
        self.producer = Producer({"bootstrap.servers": bootstrap_servers})

    def send(self, topic: str, value: bytes):
        self.producer.produce(topic=topic, value=value)

    def flush(self):
        self.producer.flush()

producer = KafkaProducerClient(KAFKA_BOOTSTRAP_SERVERS)
