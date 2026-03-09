"""
routes.py
FastAPI routes for the Ingestion Service.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from ingestion_orchestrator import orchestrator

router = APIRouter()


@router.post("/ingest")
def ingest_all():
    """Scan the image directory and process all images."""
    summarry = orchestrator.run()
    return summarry

# @router.post("/ingest/single")
# def ingest_single(file: UploadFile = File(...)):
#     """
#     Upload and process a single image.
#     Saves to IMAGE_DIRECTORY then processes it.
#     """
#     pass


@router.get("/health")
def health():
    return {"status": "healthy", "service": "ingestion-service"}
