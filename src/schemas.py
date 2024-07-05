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


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"