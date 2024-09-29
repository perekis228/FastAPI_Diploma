from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from App.backend.db_dependes import get_db
from typing import Annotated
from App.models.books import Books
from App.schemas import CreateBook, UpdateBook
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/books', tags=['books'])

@router.get('/books')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    books = db.scalars(select(Books)).all()
    return books

@router.get('/title')
async def user_by_id(db: Annotated[Session, Depends(get_db)], title: str):
    book = db.scalar(select(Books).where(Books.title == title))
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book was not found")
    return book

@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_book: CreateBook):
    db.execute(insert(Books).values(title=create_book.title,
                                    author=create_book.author,
                                    genre=create_book.genre,
                                    description=create_book.description,
                                    slug=slugify(create_book.title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], book_id: int, update_book: UpdateBook):
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
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    book = db.scalar(select(Books).where(Books.id == user_id))
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book was not found")

    db.execute(delete(Books).where(Books.id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Book delete is successful!'}