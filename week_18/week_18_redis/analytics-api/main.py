"""
Analytics API - read only analytics server

INPUT:
    - http get requests to analytics endpoints

OUTPUT:
    - json responses with aggregated alert data

FLOW:
    client -> fastapi -> redis cache / mongodb -> json response

ENDPOINTS:
    get_alerts_by_border_and_priority:
        - order boarders based on count of documents (disregarding priority)

    get_top_urgent_zones:
        - order boarders based on count or URGENT
        - top 5 

    get_distance_distribution:
        distances = "close": 0 - 300,
                    "medium": 301-800,
                    "far": 801- 1500,
                    use bucket [0, 300, 800]
        return count of each bucket

    get_low_visibility_high_activity:
        # find zones with high people count and low visibility 
            low visibility = (under 0.5)
            high people count = get avg for people count then check if bigger

    get_hot_zones:
        # find zones with high urgent count and low average distance from fence
            high urgent count = get avg for urgent count then check if bigger

"""

from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="border alerts analytics api",
    version="1.0.0"
)

app.include_router(
    router,
    prefix="/api",
    tags=["analytics"]
)


@app.get("/")
def root():
    return {"message": "analytics api is running"}