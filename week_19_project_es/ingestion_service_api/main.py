"""
main.py
Ingestion Service entry point.
"""
from fastapi import FastAPI
from routes import router

app = FastAPI(title="Ingestion Service")
app.include_router(router)


