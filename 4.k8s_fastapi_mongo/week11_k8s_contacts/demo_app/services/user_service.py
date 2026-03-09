from mongo_db import mongo_client
from models.user_model import *
from utils.mongo import to_objectId

class UserService():
    
    def get_user_collection():
        user_db = mongo_client.get_database('analiza')
        user_collection = user_db.get_collection('users')
        return user_collection
    

    @staticmethod
    def create_user(user: User) -> User:
        try:
            user_collection = UserService.get_user_collection()
            res =  user_collection.insert_one(user.model_dump(exclude={"id"}))
            if res.acknowledged:
                user = user_collection.find_one({"_id": res.inserted_id})
                if user:
                    user["id"] = str(user["_id"])
                    del user["_id"]
                    return user
            else:
                raise  ({"message": "User creation not acknowledged"})
        except Exception as e:
            raise ({"message": "Error creating user", "error": str(e)})
    
    @staticmethod
    def update_user(user: UpdateUser) -> bool:
        try:
            user_collection = UserService.get_user_collection()
            id = to_objectId(user.id)
            res = user_collection.update_one({"_id": id }, {"$set": user.model_dump(exclude={"id"})})
            if res.acknowledged:
                return True
            else:
                raise ({"message": "User update not acknowledged"})
        except Exception as e:
            raise ({"message": "Error updating user", "error": str(e)})
        
    @staticmethod
    def get_users()-> list[User]:
        try:
            user_collection = UserService.get_user_collection()
            users =  user_collection.find({})
            
            if users:
                return str(list(users))
            else:
                return []
        except Exception as e:
            raise {"message": "Error retrieving user", "error": str(e)}
        
    @staticmethod
    def delete_user(id: str)-> bool:
        try:
            user_collection = UserService.get_user_collection()
            obj_id = to_objectId(id)
            res = user_collection.delete_one({"_id": obj_id})
            if res.acknowledged:
                return True
            else:
                raise ({"message": "User deletion not acknowledged"})
        except Exception as e:
            raise {"message": "Error deleting user", "error": str(e)}
    