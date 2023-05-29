from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: int = Field(alias="_id")
    name: str
    surname: str
    mail: str
    phone: int
    role: str

