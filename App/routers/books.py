from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from App.backend.db_dependes import get_db
from typing import Annotated
from App.models.books import Books
from App.routers.users import admin as is_admin
from App.schemas import CreateBook, UpdateBook
from sqlalchemy import insert, select, update, delete
from slugify import slugify
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

router = APIRouter(prefix='/books', tags=['books'])
templates = Jinja2Templates(directory='templates')
router.mount("/static", StaticFiles(directory="static"), name="static")

@router.get('/books')
async def all_books(db: Annotated[Session, Depends(get_db)], request: Request):
    books = db.scalars(select(Books)).all()
    return templates.TemplateResponse('books.html', {'request': request, 'books': books, 'admin': is_admin})

@router.get('/{title}')
async def book_by_id(db: Annotated[Session, Depends(get_db)], title: str, request: Request):
    book = db.scalar(select(Books).where(Books.title == title))
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book was not found")
    return templates.TemplateResponse('book.html', {'request': request, 'book': book})

@router.post('/create')
async def create_book(db: Annotated[Session, Depends(get_db)], request: Request):
    form_data = await request.form()
    title = form_data.get("title")
    author = form_data.get("author")
    genre = form_data.get("genre")
    description = form_data.get("description")
    db.execute(insert(Books).values(title=title,
                                    author=author,
                                    genre=genre,
                                    description=description,
                                    slug=slugify(title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put('/update')
async def update_book(db: Annotated[Session, Depends(get_db)], book_id: int, update_book: UpdateBook):
    book = db.scalar(select(Books).where(Books.id == book_id))
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book was not found")

    db.execute(update(Books).where(Books.id == book_id).values(title=book.title,
                                                               author=book.author,
                                                               genre=book.genre,
                                                               description=update_book.description,
                                                               slug=book.slug))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Book update is successful!'}

@router.delete('/delete')
async def delete_book(db: Annotated[Session, Depends(get_db)], user_id: int):
    book = db.scalar(select(Books).where(Books.id == user_id))
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book was not found")

    db.execute(delete(Books).where(Books.id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Book delete is successful!'}