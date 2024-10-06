from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from App.backend.db_dependes import get_db
from typing import Annotated
from App.models.users import Users
from App.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

admin = False

router = APIRouter(prefix='/users', tags=['users'])
templates = Jinja2Templates(directory='templates')
router.mount("/static", StaticFiles(directory="static"), name="static")

@router.get('/register')
async def register():
    return HTMLResponse(content=open("templates/registration.html", "r").read(), status_code=200)

@router.get('/login')
async def login():
    return HTMLResponse(content=open("templates/login.html", "r").read(), status_code=200)

@router.post('/user')
async def user(db: Annotated[Session, Depends(get_db)], request: Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")

    user = db.scalar(select(Users).where(Users.username == username))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    if user.password != password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong password")
    global admin
    admin = user.admin
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], request: Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    password_repeat = form_data.get("password_repeat")
    age = form_data.get("age")

    user = db.scalar(select(Users).where(Users.username == username))
    if user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User already exist")
    if password != password_repeat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Passwords are different")
    db.execute(insert(Users).values(username=username,
                                    password=password,
                                    age=age,
                                    admin=False))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UpdateUser):
    user = db.scalar(select(Users).where(Users.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    db.execute(update(Users).where(Users.id == user_id).values(username=update_user.username,
                                                               password=update_user.password,
                                                               age=update_user.age,
                                                               admin=user.admin))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}

@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(Users).where(Users.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    db.execute(delete(Users).where(Users.id == user_id))

    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful!'}
