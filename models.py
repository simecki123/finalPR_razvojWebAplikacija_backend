from pydantic import BaseModel, Field
from typing import Optional
import bcrypt


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
    id: int
    name: str
    surname: str
    email: str
    phone: int
    role: str
    password: str

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))


    class Config:
        allow_population_by_field_name = True
        fields = {"_id": "id"}

class UserCar(BaseModel):
    id: int = Field(alias="_id")
    id_car: int
    id_user: int

    