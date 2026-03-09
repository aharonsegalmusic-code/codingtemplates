from fastapi import FastAPI
from routers import users

app = FastAPI(
    title="Simple FastAPI App",
    version="1.0.0"
)


# 🔹 Startup function (no yield)
@app.on_event("startup")
async def startup_event():
    print("🚀 Application starting...")
    # connect to DB / Kafka / Redis here


# 🔹 Include routers
app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]  # 👈 edit tag here
)


@app.get("/")
async def root():
    return {"message": "App is running"}
