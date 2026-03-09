"""
metadata_extractor.py
Extracts basic metadata from an image file and generates a unique image_id.
Constructor: logger
"""

import os
from logging import Logger
from pathlib import Path
import hashlib


from PIL import Image



class MetadataExtractor:

    def __init__(self, logger: Logger):
        self.logger = logger

    def extract_metadata(self, image_path: str) -> dict:
        """
        Extract basic metadata from the image file.

        Returns:
            dict with keys: filename, file_size, width, height, format
        """
        with Image.open(image_path) as img:
            metadata = {
                "filename": os.path.basename(image_path),
                "format": img.format,
                "width": img.size[0],
                "height": img.size[1],
                "mode": img.mode,             
                "file_size": os.path.getsize(image_path),
            }
            return metadata

    def generate_image_id(self, image_path: str) -> str:
        """
        Generate a unique ID from file content.
        Same file = same ID.
        """
        # open file in binary mode and read all bytes
        with open(image_path, "rb") as f:
            file_bytes = f.read()

        # hashlib.sha256(file_bytes)  → creates a hash object from the bytes
        # .hexdigest()                → converts hash to a 64-character string like "a3f2b1c8..."
        # [:16]                       → take first 16 characters — short but still unique
        image_id = hashlib.sha256(file_bytes).hexdigest()[:16]
        return image_id
