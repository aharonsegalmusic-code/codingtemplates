# main.py
from fastapi import FastAPI

from routes_overview import router as overview_router
from routes_query_main import router as query_router
from mongo_db import MongoDB
import mongo_insert as mi

app = FastAPI(title="FastAPI + Mongo")

# Group 1: overview endpoints
app.include_router(
    overview_router,
    prefix="/overview",
    tags=["overview"],
)

# Group 2: query endpoints
app.include_router(
    query_router,
    prefix="/query",
    tags=["query"],
)

@app.on_event("startup")
def startup() -> None:
    # 1) Connect (MongoDB reads env inside __init__)
    mongo = MongoDB()

    # 2) Check connection (blocks startup, raises if broken)
    mongo.ping()

    # 3) Insert JSON files on startup (learning mode)
    # NOTE: this will insert again if you restart the app unless you guard it (see below).
    report = mi.insert_all_json_files(mongo.db)
    print("Startup insert report:", report)

    # 4) Save for routes
    app.state.mongo = mongo


@app.on_event("shutdown")
def shutdown() -> None:
    mongo = getattr(app.state, "mongo", None)
    if mongo is not None:
        mongo.close()