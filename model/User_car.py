from pydantic import BaseModel, Field
from typing import Optional

class User_car(BaseModel):
    id: int = Field(alias="_id")
    id_car: int
    id_user: int
    