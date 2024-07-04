from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field

class ContactModel(BaseModel):
    name: str = Field(max_length=20)
    surname: str = Field(max_length=20)
    email: str = Field(max_length=30)
    phone: str = Field(max_length=12)
    birthday: date = Field()
    addition_info: Optional[str] = Field(max_length=100, default=None)

class ContactResponse(ContactModel):
    id: int

class ContactUpdate(ContactModel):
    done: bool


class TagModel(BaseModel):
    name: str = Field(max_length=25)

class TagResponse(TagModel):
    id: int

    class Config:
        orm_mode = True

class NoteBase(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=150)

class NoteModel(NoteBase):
    tags: List[int]

class NoteUpdate(NoteModel):
    done: bool

class NoteStatusUpdate(BaseModel):
    done: bool

class NoteResponse(NoteBase):
    id: int
    created_at: datetime
    tags: List[TagResponse]

    class Config:
        orm_mode = True
