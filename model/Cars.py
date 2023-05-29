from pydantic import BaseModel, Field
from typing import Optional

class Cars(BaseModel):
    id: int = Field(alias="_id")
    name: str
    mark: str
    price: int
    reserved: bool