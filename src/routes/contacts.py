from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse, ContactUpdate
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=["contacts"])

@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)

@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts

@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.get("/search/{search_string}", response_model=List[ContactResponse])
async def search_contacts(search_string: str, db: Session = Depends(get_db)):
    contacts = await repository_contacts.search_contacts(search_string, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contacts not found")
    return contacts

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactUpdate, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    return contact

@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    return contact

@router.get("/close_birthdays/", response_model=List[ContactResponse])
async def close_birthdays(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_close_birthdays(7,db)
    return contacts