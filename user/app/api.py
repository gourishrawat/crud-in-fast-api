from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from . models import *
from json import JSONEncoder
from fastapi.encoders import jsonable_encoder

from passlib.context import CryptContext
from fastapi_login.exceptions import InvalidCredentialsException

from fastapi_login import LoginManager
from .pydentic_models import Person, Loginperson,Delete
import uuid
import typing

SECRET = 'your-secret-key'

app = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
manager = LoginManager(SECRET, token_url='/auth/token')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

@app.post("/ragistration_api/")
async def ragistration(data: Person):
    if await User.exists(phone=data.phone):
        return {"status": False, "message": "phone number already exists"}
    elif await User.exists(email=data.email):
        return {"status": False, "message": "email already exists"}
    else:
        user_obj = await User.create(email=data.email, name=data.name,
                                     phone=data.phone, password=get_password_hash(data.password))
        return user_obj

@app.get("/data/")
async def all_user():
    user = await User.all()
    return user

@app.delete("/delete_user/{id}")
async def delete(data:Delete):
    user_obj = await User.get(id  = data.id).delete()
    return{"status": True, "message":"user delete"}


