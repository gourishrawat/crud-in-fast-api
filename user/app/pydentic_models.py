from pydantic import BaseModel


class Person(BaseModel):
    email:str
    name:str
    phone:int
    password:str


class Loginperson(BaseModel):
    email : str
    password : str

class Delete(BaseModel):
    id : int

# class Get_person(BaseModel):
#     id : int

