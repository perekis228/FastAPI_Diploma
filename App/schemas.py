from pydantic import BaseModel

class CreateBook(BaseModel):
    title: str
    author: str
    genre: str
    description: str


class UpdateBook(BaseModel):
    description: str