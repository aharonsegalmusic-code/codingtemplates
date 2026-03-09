"""
ingestion_orchestrator.py
Scans the local image directory, processes each image end-to-end.
Constructor: config, ocr_engine, metadata_extractor, Gridfs, publisher, logger
"""

import os
import sys
from logging import Logger
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.logger import get_logger
from ingestion_config import IngestionConfig
from OCRengine import OCREngine
from metadata_extractor import MetadataExtractor
from mongo_client import MongoLoaderClient
from shared.kafka_publisher import KafkaPublisher

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif", ".webp"}


class IngestionOrchestrator:

    def __init__(
        self,
        config: IngestionConfig,
        ocr_engine: OCREngine,
        metadata: MetadataExtractor,
        Gridfs: MongoLoaderClient,
        publisher: KafkaPublisher,
        logger: Logger,
    ):
        self.config = config
        self.ocr_engine = ocr_engine
        self.metadata_extractor = metadata
        self.Gridfs = Gridfs
        self.publisher = publisher
        self.logger = logger

    def process_image(self, path: str) -> None:
        """
        Process a single image end-to-end:
        1. Generate image_id
        2. Extract metadata
        3. Run OCR
        4. Send binary to GridFS service
        5. Publish RAW event to Kafka
        """
        filename = Path(path).name
        self.logger.info("Processing image: %s", filename)

        try:
            # 1. generate unique image_id
            image_id = self.metadata_extractor.generate_image_id(path)

            # 2. extract metadata
            metadata = self.metadata_extractor.extract_metadata(path)

            # 3. run OCR
            raw_text = self.ocr_engine.extract_text(path)
    
            # 4. publish RAW event
            event = {
                "image_id": image_id,
                "raw_text": raw_text,
                "metadata": metadata,
            }
            self.publisher.publish(event)

            # 5. send binary file to GridFS service
            self.Gridfs.send(path, image_id)


            self.logger.info("Finished processing image_id=%s (%s)", image_id, filename)

        except Exception as e:
            self.logger.error("Failed to process %s: %s", filename, e)

    def run(self) -> dict:
        """
        Scan the image directory and process all image files.

        Returns:
            Summary dict with processed/failed counts.
        """
        image_dir =self.config.image_directory
        self.logger.info("Scanning image directory: %s", image_dir)

        files = [
            os.path.join(image_dir, f)
            for f in os.listdir(image_dir)
            if Path(f).suffix.lower() in IMAGE_EXTENSIONS
        ]

        self.logger.info("Found %d image files", len(files))

        processed = 0
        failed = 0

        for file_path in files:
            try:
                self.process_image(file_path)
                processed += 1
            except Exception:
                failed += 1

        summary = {"processed": processed, "failed": failed, "total": len(files)}
        self.logger.info("Ingestion complete: %s", summary)
        return summary


# ---- wiring ----
_logger = get_logger("ingestion-service")
_config = IngestionConfig()

orchestrator = IngestionOrchestrator(
    config=_config,
    ocr_engine=OCREngine(_logger),
    metadata=MetadataExtractor(_logger),
    Gridfs=MongoLoaderClient(_config.gridfs_service_url, _logger),
    publisher=KafkaPublisher(_config.bootstrap_servers, _config.kafka_topic_raw, _logger),
    logger=_logger,
)