from fastapi import APIRouter, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from passlib.context import CryptContext
from . models import User
import typing
import passlib
from fastapi_login import LoginManager
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException


SECRET = 'your-secret-key'

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
manager = LoginManager(SECRET, token_url='/auth/token')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# def flash(request: Request, message: typing.Any, category: str = "") -> None:
#     if "_messages" not in request.session:
#         request.session["_messages"] = []
#     request.session["_messages"].append({"message": message, "category": category})


# def get_flashed_messages(request: Request):
#     print(request.session)
#     return request.session.pop("_messages") if "_messages" in request.session else []


@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, })

# login page render
@router.get("/login/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, })

@router.get("/welcome/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("welcome.html",
                                       {"request": request, })


@router.post("/registration/", response_class=HTMLResponse)
async def read_item(request: Request, email: str = Form(...),
                    name: str = Form(...),
                    phone: str = Form(...),
                    password: str = Form(...)):
    if await User.filter(email=email).exists():
        # flash(request , "Email already exists")
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

    elif await User.filter(phone=phone).exists():
        # flash(request , "Phone number already exists")
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

    else:
        await User.create(email=email, name=name, phone=phone,
                          password=get_password_hash(password))
        # flash(request , "Successfully register")
        return RedirectResponse("/login/", status_code=status.HTTP_302_FOUND)
    
# login manager 


@manager.user_loader()
async def load_user(email: str):  # could also be an asynchronous function
    if await User.exists(email=email):
      user = await User.get(email=email)
      return user

@router.post('/auth/token')
async  def logins(request: Request,email:str = Form(...),
                 Password: str = Form(...)):
    email = email
    user = await load_user(email)
    if not user:
        return{'USER NOT REGISTER'}
    elif not verify_password (Password,user.password):
        return{'PASSWORD IS WRONG'}
    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    if "_messages" not in request.session:
        request.session['_messages'] = []
        new_dict = {"user_id": str(
            user.id),"email":email, "access_token":str(access_token)}
        request.session['_messages'].append(
            new_dict
        )
        print(new_dict)
    return RedirectResponse('/welcome/', status_code=status.HTTP_302_FOUND)