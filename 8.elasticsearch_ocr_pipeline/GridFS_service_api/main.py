from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="GridFS api",
    version="1.0.0"
)

app.include_router(
    router,
    prefix="/api",
    tags=["GridFS"]
)


@app.get("/")
def root():
    return {"message": "GridFS api is running"}