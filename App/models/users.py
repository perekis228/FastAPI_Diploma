from sqlalchemy import Column, Integer, String, Boolean
from App.backend.db import Base


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    age = Column(String)
    admin = Column(Boolean, default=False)

from sqlalchemy.schema import CreateTable
print(CreateTable(Users.__table__))