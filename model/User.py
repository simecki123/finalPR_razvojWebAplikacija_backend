from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: int
    name: str
    surname: str
    mail: str
    phone: int

