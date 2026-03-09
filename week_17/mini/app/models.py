""""
== INPUT EXAMPLE ==
  {
    "user_id": "00000000-0000-4000-8000-000000000001",
    "full_name": "Aviv Katz",
    "email": "aviv.katz1@example.com",
    "age": 30,
    "phone": "0532181960",
    "city": "Beer Sheva",
    "created_at": "2026-01-01T09:00:00Z",
    "posts": [
      {
        "post_id": "p0001-01",
        "title": "Validation with Pydantic",
        "published_at": "2026-01-09T16:45:00Z",
        "content": "Thoughts on batching and rate limiting."
      }
    ]
  }
"""
from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class PostModel(BaseModel):

    post_id: str = Field(
        ...,
        pattern=r"^p\d{4}-\d{2}$",  # example: p0001-01
        description='Format: "p0001-01"',
    )
    title: str = Field(..., min_length=1)
    published_at: datetime  # accepts "2026-01-01T09:00:00Z" and converts to datetime
    content: str = Field(..., min_length=1)


class UserRegisterModel(BaseModel):

    user_id: str = Field(
        ...,
        pattern=r"^\d{8}-\d{4}-\d{4}-\d{4}-\d{12}$",
        description='UUID string format: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"',
    )
    full_name: str = Field(..., min_length=1)
    email: EmailStr  
    age: int = Field(..., ge=0, le=120)  # >= 0 and <= 120
    phone: str = Field(..., pattern=r"^\d+$", description='Digits only, e.g. "0585149368"')
    city: str = Field(..., min_length=1)
    created_at: datetime  # accepts ISO string and converts to datetime

    posts: List[PostModel]



