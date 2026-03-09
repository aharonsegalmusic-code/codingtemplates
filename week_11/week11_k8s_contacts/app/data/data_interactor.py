"""
STATUS: BASIC LEVEL COMPLETE
    TODO: - add unique phone number checker
        - implement that function in the create and update functions

This file handles AND all CRUD operations:

create_contact(contact: dict) → returns new contact ID as string
get_all_contacts() → returns list of Contact objects
update_contact(id: str, contact: dict) → returns success boolean
delete_contact(id: str) → returns success boolean

Handles errors with appropriate HTTP status codes

preview of a contact in the db:
    {'_id': ObjectId('6953af2451d6e1be82767fd1'), 
    'first_name': 'Korey', 
    'last_name': 'Steward', 
    'phone_number': '077-7934083'}
"""
from typing import List
from data.db_use import db
from pymongo import ReturnDocument
from bson.objectid import ObjectId

# ------------------------
# contact fields to dict
# ------------------------
def to_dict(first_name,last_name,phone_number) -> dict:
    return {
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
    }

# ------------------------
# CRUD Functions
# ------------------------
"""
- Gets contact input from create_contact()
- Converts input to dict 
- Adds the contact to the db
- Returns new contact id
"""
def create_contact(first_name: str, last_name: str, phone_number: str) -> int:
    contact_dict = to_dict(first_name,last_name,phone_number)
    result = db.Contacts.insert_one(contact_dict)
    return str(result.inserted_id)

def get_all_contacts() -> List: 
    contacts = db.Contacts.find()
    # contacts is a object <pymongo.synchronous.cursor.Cursor object>
    # convert this obj to list
    return list(contacts)

def get_contact_by_id(contact_id: ObjectId) -> dict | None:
    contact = db.Contacts.find_one({"_id": contact_id})
    return contact

def delete_contact_by_id(contact_id: ObjectId) -> bool:
    """
    - Deletes contact by _id.
    - Returns True if a contact was deleted else False
    """
    result = db.Contacts.delete_one({"_id": contact_id})
    return result.deleted_count > 0


def update_contact_by_id(contact_id: ObjectId, contact: dict) -> dict | None:
    """
    - Updates fields in contact on the contact with _id == contact_id
    - Returns the updated contact or None if not found.
    """
    result = db.Contacts.find_one_and_update(
        {"_id": contact_id},
        {"$set": contact},
        return_document=ReturnDocument.AFTER,  # return updated contact
    )
    return result
