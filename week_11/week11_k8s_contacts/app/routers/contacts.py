"""
STATE : COMPLETE
this file is the router that communicates with db functions 
    it gets input and requests from the user
    and sends a processed request to the db functions

routes included 
    create_contact
    list_contacts
    get_contact_by_id
    update_contact_by_id
    delete_contact
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel, Field
from typing import Optional
from bson.objectid import ObjectId
from data.data_interactor import (
    create_contact as db_create_contact,
    get_all_contacts as db_get_all_contacts,
    get_contact_by_id as db_get_contact_by_id,
    delete_contact_by_id as db_delete_contact_by_id,
    update_contact_by_id as db_update_contact_by_id,
)

router = APIRouter(prefix="/contacts", tags=["Contacts"])

# ------------------------
# Pydantic Models / Schemas
# ------------------------
class ContactSchema(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    phone_number: str = Field(min_length=1, max_length=20)


class ContactResponse(ContactSchema):
    id: str

class ContactUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    phone_number: Optional[str] = Field(default=None, min_length=1, max_length=20)

# ------------------------
# Helpers
# ------------------------
"""
Converts MongoDB document into a Py dict
dict of contact including id
"""
def contact_to_dict(contact: dict) -> dict:
    return {
        "id": str(contact["_id"]),
        "first_name": contact["first_name"],
        "last_name": contact["last_name"],
        "phone_number": contact["phone_number"],
    }

def validate_ObjectId(contact_id: str)-> ObjectId:
    # validate ObjectId
    if not ObjectId.is_valid(contact_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid contact id",
        )
    else:
        return ObjectId(contact_id)
    
# ------------------------
# API Endpoints
# ------------------------
"""
- Gets contact from user
- Sends it to db_create_contact()
- Contact added to the db 
- Gets from it generated id
- Return the generated id
"""
@router.post("/")
def create_contact(contact: ContactSchema):
    try:
        # send to the db 
        new_id = db_create_contact(
            contact.first_name,
            contact.last_name,
            contact.phone_number,
        )
        return {"message": "Contact created successfully", "id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""
- Returns Contact collection list
"""
@router.get("/", response_model=list[ContactResponse])
def list_contacts():
    try:
        contacts = db_get_all_contacts()
        return [contact_to_dict(c) for c in contacts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""
- Gets contact id: str 
    ex: "6953af2451d6e1be82767fbe"
- Returns that contact as dict
"""
@router.get("/{contact_id}",response_model=ContactResponse)
def get_contact_by_id(contact_id:str):

    # validate and return ObjectId
    oid = validate_ObjectId(contact_id)

    # request from db
    contact = db_get_contact_by_id(oid)
    result = contact_to_dict(contact)
    return result

"""
- Gets contact_id: str
- Check existance of contact
- Send input to db_update_contact_by_id
- Updates that contact and returns the updated contact as dict
- Returns status code
"""
@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact_by_id(contact_id: str, contact: ContactUpdate):

    # validate and return ObjectId
    oid = validate_ObjectId(contact_id)

    # check existing
    existing = db_get_contact_by_id(oid)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )
    
    # make update_data from the Pydantic model (only provided fields)
    update_data = contact.model_dump(exclude_unset=True)

    # if nothing to update -> return existing
    if not update_data:
        return contact_to_dict(existing)

    # send to update
    updated_contact = db_update_contact_by_id(oid, update_data)

    # Convert to dict/response model
    result = contact_to_dict(updated_contact)
    return result

"""
- Gets contact_id: int
- Send that id to 
- Deletes that contact to db_delete_contact_by_id()
- Gets True or False stating the deletion 
- Returns status code
"""
@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: str):

    # validate and return ObjectId
    oid = validate_ObjectId(contact_id)

    # send to db
    deleted = db_delete_contact_by_id(ObjectId(oid))

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)