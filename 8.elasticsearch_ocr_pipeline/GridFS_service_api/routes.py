import json
from fastapi import APIRouter
from dotenv import dotenv_values


config = dotenv_values(".env")


router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
)


@router.post("/upload")        # ← same path, same method
def upload(file: UploadFile, image_id: str):
    """
    get from Ingestion a file to be uploaded
    """