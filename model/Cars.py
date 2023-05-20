from pydantic import BaseModel, Field
from typing import Optional

class Cars(BaseModel):
    id: int
    name: str
    mark: str
    price: int
    reserved: bool