from fastapi import FastAPI
from routers.basic_test import router as db_test_router
from routers.contacts import router as crud

app = FastAPI(title="Contacts Manager")

# register routers
app.include_router(db_test_router)
app.include_router(crud)

