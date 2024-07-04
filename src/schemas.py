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