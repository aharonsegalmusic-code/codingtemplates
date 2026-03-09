from fastapi import APIRouter, status, Body, Query
from typing import Annotated
from models.user_model import *
from services.user_service import *

router = APIRouter()

# @app.post("/users",status_code=status.HTTP_201_CREATED)
@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(user: Annotated[User,Body(embed=True,strict=True)]):
    try:
        user = UserService.create_user(user)
        if user:
            return {"message": "User created", "user": user}
        else:
            return ({"message": "User creation not acknowledged"})
    except Exception as e:
        return ({"message": "Error creating user", "error": str(e)})
    
# @app.put("/users",status_code=status.HTTP_201_CREATED)
@router.put("/",status_code=status.HTTP_201_CREATED)
async def update_user(user: Annotated[UpdateUser,Body(embed=True, strict=True)]):
    try:
        is_updated_user = UserService.update_user(user)
        if is_updated_user:
            return {"message": "User updated"}
        else:
            return ({"message": "User update not acknowledged"})
    except Exception as e:
        return ({"message": "Error updating user", "error": str(e)})

# @app.get("/users",status_code=status.HTTP_200_OK)
@router.get("/",status_code=status.HTTP_200_OK)
async def get_user():
    try:
        users = UserService.get_users()
        if users:
            return {"message": "Users found", "users": users}
        else:
            return {"message": "User not found"}
    except Exception as e:
        return {"message": "Error retrieving user", "error": str(e)}

# @app.delete("/users",status_code=status.HTTP_200_OK)
@router.delete("/",status_code=status.HTTP_200_OK)
async def delete_user(id: Annotated[str, Query(strict=True) ]):
    try:
        is_deleted_user = UserService.delete_user(id)
        if is_deleted_user:
            return {"message": "User deleted"}
        else:
            return ({"message": "User deletion not acknowledged"})
    except Exception as e:
        return {"message": "Error deleting user", "error": str(e)}