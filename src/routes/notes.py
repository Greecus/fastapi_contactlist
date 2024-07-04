from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse, ContactUpdate
from src.repository import notes as repository_notes

router = APIRouter(prefix='/notes', tags=["notes"])

@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    return await repository_notes.create_contact(body, db)

@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notes = await repository_notes.get_contacts(skip, limit, db)
    return notes

@router.get("/{note_id}", response_model=ContactResponse)
async def read_contact(note_id: int, db: Session = Depends(get_db)):
    note = await repository_notes.get_contact(note_id, db)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return note

@router.get("/search/{search_string}", response_model=List[ContactResponse])
async def search_contacts(search_string: str, db: Session = Depends(get_db)):
    notes = await repository_notes.search_contacts(search_string, db)
    return notes

@router.put("/{note_id}", response_model=ContactResponse)
async def update_contact(body: ContactUpdate, note_id: int, db: Session = Depends(get_db)):
    note = await repository_notes.update_contact(note_id, body, db)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note

@router.delete("/{note_id}", response_model=ContactResponse)
async def remove_contact(note_id: int, db: Session = Depends(get_db)):
    note = await repository_notes.remove_contact(note_id, db)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note

@router.get("/close_birthdays/{limit}", response_model=List[ContactResponse])
async def close_birthdays(limit: int = 7,db: Session = Depends(get_db)):
    notes = await repository_notes.get_close_birthdays(limit,db)
    return notes