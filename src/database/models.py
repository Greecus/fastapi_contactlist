from sqlalchemy import Column, Integer, String, Boolean, func, Table, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contact"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    surname = Column(String(20), nullable=False)
    email = Column(String(30), nullable=False)
    phone = Column(String(12), nullable=False)
    birthday = Column(Date, nullable=False)
    addition_info = Column(String(100), nullable=True)