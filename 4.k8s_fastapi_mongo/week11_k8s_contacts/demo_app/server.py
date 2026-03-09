from fastapi import FastAPI
from routes.user import router as user_router

def server_init():
    app = FastAPI()
    app.include_router(router=user_router, prefix="/users", tags=["users"])
    return app

app = server_init()
