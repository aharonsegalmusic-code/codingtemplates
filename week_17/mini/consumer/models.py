from typing import Optional
from datetime import datetime
from beanie import Document
from pydantic import EmailStr, Field

class User(Document):
    full_name: str
    email: EmailStr
    age: int
    phone: Optional[str] = None
    city: Optional[str] = None
    insertion_time: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "mini_users"
