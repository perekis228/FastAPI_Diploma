#python -m uvicorn App.main:app
from fastapi import FastAPI
from App.routers import books, users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(books.router)
app.include_router(users.router)