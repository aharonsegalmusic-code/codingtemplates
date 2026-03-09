"""
ingestionConfig.py
Loads environment variables for the Ingestion Service.
Constructor: no params — loads from env.
"""

import os


class IngestionConfig:

    def __init__(self):
        self.image_directory = os.getenv("IMAGE_DIRECTORY", "images")
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.kafka_topic_raw = os.getenv("KAFKA_TOPIC_RAW", "raw")
        self.gridfs_service_url = os.getenv("GRIDFS_SERVICE_URL", "http://localhost:8001")

config = IngestionConfig()