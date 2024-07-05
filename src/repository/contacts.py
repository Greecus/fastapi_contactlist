from typing import List

from sqlalchemy import or_, and_, extract
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactUpdate

from datetime import date, timedelta

async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    contact = Contact(name=body.name, surname=body.surname, email=body.email, phone=body.phone, birthday=body.birthday, user=user, addition_info=body.addition_info)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()

async def get_contact(id: int, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(and_(Contact.id == id,Contact.user_id == user.id)).first()

async def search_contacts(match_str: str, user: User, db: Session) -> List[Contact] | None:
    matching_contacts = list() 
    matching_contacts.extend(db.query(Contact).filter(and_(Contact.name == match_str,Contact.user_id == user.id)).all())
    matching_contacts.extend(db.query(Contact).filter(and_(Contact.surname == match_str,Contact.user_id == user.id)).all())
    matching_contacts.extend(db.query(Contact).filter(and_(Contact.email == match_str,Contact.user_id == user.id)).all())
    if not matching_contacts: return None
    return matching_contacts

async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id,Contact.user_id == user.id)).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.addition_info = body.addition_info
        db.commit()
    return contact

async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id,Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def get_close_birthdays(limit:int, user: User, db: Session) -> List[Contact]:
    today = date.today()
    end_day = date.today() + timedelta(days=limit)
    return db.query(Contact).filter(and_(or_(
        and_(extract('month', Contact.birthday) == today.month,
             extract('day', Contact.birthday) >= today.day),
        and_(extract('month', Contact.birthday) == end_day.month,
             extract('day', Contact.birthday) <= end_day.day)),Contact.user_id == user.id)).all()