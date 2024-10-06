from pydantic import BaseModel

class CreateBook(BaseModel):
    title: str
    author: str
    genre: str
    description: str


class UpdateBook(BaseModel):
    description: str

class CreateUser(BaseModel):
    username: str
    password: str
    password_repeat: str
    age: str
    admin: bool

class UpdateUser(BaseModel):
    username: str
    password: str
    age: str