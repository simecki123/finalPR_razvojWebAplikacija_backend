from pydantic import BaseModel, Field
from typing import Optional

class Cars(BaseModel):
    id: int
    name: str
    mark: str
    price: int
    reserved: bool

    class Config:
        allow_population_by_field_name = True
        fields = {"_id": "id"}

class User(BaseModel):
    id: int = Field(alias="_id")
    name: str
    surname: str
    mail: str
    phone: int
    role: str

class UserCar(BaseModel):
    id: int = Field(alias="_id")
    id_car: int
    id_user: int

    