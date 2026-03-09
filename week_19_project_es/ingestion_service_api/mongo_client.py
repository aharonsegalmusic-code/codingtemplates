"""
Sends the binary file to the GridFS Service via HTTP POST.
Constructor: gridfs_service_url, logger
"""

from logging import Logger
from pathlib import Path
import requests

class MongoLoaderClient:

    def __init__(self, gridfs_service_url: str, logger: Logger):
        self.gridfs_service_url = gridfs_service_url.rstrip("/")
        self.logger = logger

    def send(self, file_path: str, image_id: str) -> dict:
        """
        POST the binary file to the GridFS service.

        Args:
            file_path: Path to the image file.
            image_id:  Unique identifier for the image.

        Returns:
            Response JSON from the GridFS service.
        """
        filename = Path(file_path).name
        url = f"{self.gridfs_service_url}/upload"

        self.logger.info("Sending %s (image_id=%s) to %s", filename, image_id, url)

        # open file in binary mode and send as multipart form data
        # files = the binary image
        # data  = the image_id so GridFS knows what to name it
        with open(file_path, "rb") as f:
            response = requests.post(
                url,
                files={"file": (filename, f)},
                data={"image_id": image_id},
                timeout=30,
            )

        # raise an exception if status code is 4xx or 5xx
        response.raise_for_status()

        self.logger.info("Upload success for image_id=%s", image_id)
        return response.json()

