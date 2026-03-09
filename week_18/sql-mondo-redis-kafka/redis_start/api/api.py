"""
gets orders from json
    adds status field
    set ot to "PREPARING"
    inserts to mogno

"""

from fastapi import FastAPI

from .router import router
from .health_routes import health_router

# uvicorn api.api:app --reload

app = FastAPI(
    title="PIZZA ORDER ;)",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    print("Application starting...")


# main routes
app.include_router(
    router,
    prefix="/api",
    tags=["start_data"]
)

# health check routes
app.include_router(
    health_router,
    prefix="/api",
    tags=["health"]
)


@app.get("/")
async def root():
    return {"message": "App is running"}