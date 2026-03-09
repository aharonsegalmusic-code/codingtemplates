"""
API Gateway Service (FastAPI)

INPUT:
    - POST /api/file_data/uploadfile  -> receives a JSON file with pizza orders
    - GET  /api/file_data/order/{id}  -> returns a single order by order_id

OUTPUT:
    - saves each order to MongoDB with status="PREPARING"
    - publishes each order to Kafka topic "pizza_orders"
    - returns order data (from Redis cache or MongoDB fallback)

FLOW:
    Client -> API -> MongoDB (store)
                  -> Kafka "pizza_orders" (publish)
    Client -> API -> Redis (cache check) -> MongoDB (fallback)
"""

from fastapi import FastAPI

from .router import router
from .health_routes import health_router

# run locally: uvicorn api.api:app --reload

app = FastAPI(
    title="PIZZA ORDER ;)",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    print("API Gateway starting...")


# main routes - file upload + order lookup
app.include_router(
    router,
    prefix="/api",
    tags=["start_data"]
)

# health check routes - ping each service
app.include_router(
    health_router,
    prefix="/api",
    tags=["health"]
)


@app.get("/")
async def root():
    return {"message": "App is running"}
