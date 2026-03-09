# app/routers/public.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(
    prefix="/public",
    tags=["public"],
)


class EchoRequest(BaseModel):
    message: str


class User(BaseModel):
    id: int
    name: str


# some in-memory data just for demo (no DB)
FAKE_USERS = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
]


@router.get("/ping")
def ping():
    return {"status": "ok"}


@router.get("/users", response_model=List[User])
def get_users():
    # just returns the in-memory list
    return FAKE_USERS


@router.get("/users/{user_id}", response_model=User | None)
def get_user(user_id: int):
    for user in FAKE_USERS:
        if user["id"] == user_id:
            return user
    return None


@router.post("/echo")
def echo(payload: EchoRequest):
    # just returns the same message back
    return {"echo": payload.message}