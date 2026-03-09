"""
loads env 
    -   related to kafka
    READ TOPIC: "raw"
    WRITE TOPIC: "Clean" 
"""
import os


class CleanConfig:

    def __init__(self):
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")
        self.clean_group = os.getenv("KAFKA_GROUP_CLEAN", "cleaning_group")
        self.kafka_topic_raw = os.getenv("KAFKA_TOPIC_RAW", "raw")
        self.kafka_topic_clean = os.getenv("KAFKA_TOPIC_CLEAN", "clean")


