from pydantic import StringConstraints , BaseModel, UUID1 
from typing import Annotated
from utils.regex import email_regex


class User(BaseModel):
    # Config_Dict class , advanced pydantic configuration
    model_config = {"extra": "forbid" ,"strict":True}

    id: Annotated[UUID1, "Creation Parameter"] = None
    name: Annotated[str, StringConstraints(min_length=3, max_length=50)]
    email: Annotated[str, StringConstraints(pattern=email_regex(),min_length=5, max_length=100)]

class UpdateUser(BaseModel):
    model_config = {"extra": "forbid"}
    id: Annotated[str, "Creation Parameter"]
    #Optional fields can use Optional param in typing library or default to None
    name: Annotated[str, StringConstraints(min_length=3, max_length=50)] | None = None
    email: Annotated[str, StringConstraints(pattern=email_regex(),min_length=5, max_length=100)] | None = None
