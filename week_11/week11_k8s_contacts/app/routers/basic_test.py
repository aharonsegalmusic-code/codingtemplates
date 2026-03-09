from fastapi import APIRouter
from data.db_use import basic_crud_test

router = APIRouter(prefix="/test",tags=["DB Test"])

# api util test
@router.get("/health", status_code=201)
def health():
    return {"status": "ok"}

# MongoDB connection test 
@router.get("/db")
def test_db_connection():
    result = basic_crud_test()
    return result



