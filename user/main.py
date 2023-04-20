from fastapi import FastAPI
from app import router as UsersRoute
from tortoise.contrib.fastapi import register_tortoise
from app import api as apirouter



app = FastAPI()
app.include_router(UsersRoute.router)
app.include_router(apirouter.app,tags=["api"])



# @app.get("/")
# def read_root():
#     return {"hellow": "world"}  # jason formate


register_tortoise(
    app,
    db_url="postgres://postgres:root@127.0.0.1/crud-fastapi",
    modules={'models': ['app.models',]},
    generate_schemas=True,
    add_exception_handlers=True,

)
