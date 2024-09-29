#python -m uvicorn App.main:app
from fastapi import FastAPI, Depends, status, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from App.routers import books
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from App.backend.db_dependes import get_db
from typing import Annotated
from App.models.books import Books
from sqlalchemy import select

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)], request: Request):
    books = db.scalars(select(Books)).all()
    return templates.TemplateResponse('books.html', {'request': request, 'books': books})

@app.get('/{title}')
async def user_by_id(db: Annotated[Session, Depends(get_db)], title: str, request: Request):
    book = db.scalar(select(Books).where(Books.title == title))
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book was not found")

    return templates.TemplateResponse('book.html', {'request': request, 'book': book})

app.include_router(books.router)