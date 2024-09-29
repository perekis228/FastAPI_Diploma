from sqlalchemy import Column, Integer, String
from App.backend.db import Base

class Books(Base):
    __tablename__ = 'books'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)
    description = Column(String)
    slug = Column(String, unique=True, index=True)

from sqlalchemy.schema import CreateTable
print(CreateTable(Books.__table__))