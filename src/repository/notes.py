from typing import List

from sqlalchemy import or_, and_, extract
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel, ContactUpdate
#from src.schemas import NoteModel, NoteUpdate, NoteStatusUpdate
#from src.database.models import Note, Tag

from datetime import date, datetime, timedelta

async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(name=body.name, surname=body.surname, email=body.email, phone=body.phone, birthday=body.birthday, addition_info=body.addition_info)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()

async def get_contact(id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == id).first()

async def search_contacts(match_str: str, db: Session) -> List[Contact] | None:
    matching_contacts = list() 
    matching_contacts.extend(db.query(Contact).filter(Contact.name == match_str).all())
    matching_contacts.extend(db.query(Contact).filter(Contact.surname == match_str).all())
    matching_contacts.extend(db.query(Contact).filter(Contact.email == match_str).all())
    if not matching_contacts: return None
    return matching_contacts

async def update_contact(note_id: int, body: ContactUpdate, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == note_id).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.addition_info = body.addition_info
        db.commit()
    return contact

async def remove_contact(note_id: int, db: Session) -> Contact | None:
    note = db.query(Contact).filter(Contact.id == note_id).first()
    if note:
        db.delete(note)
        db.commit()
    return note

async def get_close_birthdays(limit:int, db: Session) -> List[Contact]:
    today = date.today()
    end_day = date.today() + timedelta(days=limit)
    return db.query(Contact).filter(or_(
        and_(extract('month', Contact.birthday) == today.month,
             extract('day', Contact.birthday) >= today.day),
        and_(extract('month', Contact.birthday) == end_day.month,
             extract('day', Contact.birthday) <= end_day.day))).all()
    
'''async def get_notes(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()

async def get_note(note_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == note_id).first()

async def create_note(body: NoteModel, db: Session) -> Contact:
    tags = db.query(Tag).filter(Tag.id.in_(body.tags)).all()
    note = Contact(title=body.title, description=body.description, tags=tags)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

async def remove_note(note_id: int, db: Session) -> Note | None:
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        db.delete(note)
        db.commit()
    return note

async def update_note(note_id: int, body: NoteUpdate, db: Session) -> Note | None:
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        tags = db.query(Tag).filter(Tag.id.in_(body.tags)).all()
        note.title = body.title
        note.description = body.description
        note.done = body.done
        note.tags = tags
        db.commit()
    return note

async def update_status_note(note_id: int, body: NoteStatusUpdate, db: Session) -> Note | None:
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        note.done = body.done
        db.commit()
    return note'''
