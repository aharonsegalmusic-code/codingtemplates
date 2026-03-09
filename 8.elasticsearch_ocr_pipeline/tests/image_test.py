from PIL import Image, ExifTags
import pytesseract
from PIL.ExifTags import TAGS
import os
import hashlib
from pprint import pprint


dir_path = "ingestion_service_api\images"
image_path = "tweet_0.png"

def extract_metadata(image_path: str) -> dict:
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

def generate_image_id(image_path: str) -> str:
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


def extract_text(image_path: str) -> str:
    """
    Run OCR on the given image file.

    Args:
        image_path: Path to the image file.

    Returns:
        raw_text extracted from the image.
    """
    try:
        img = Image.open(image_path)
        raw_text = pytesseract.image_to_string(img)
        return raw_text

    except Exception as e:
        raise

metadata = extract_metadata(image_path)
image_id = generate_image_id(image_path)
raw_text = extract_text(image_path)
event = {
    "image_id": image_id,
    "raw_text": raw_text,
    "metadata": metadata,
}
print("-----------EVENT--------------")
pprint(event)