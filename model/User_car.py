from pydantic import BaseModel, Field
from typing import Optional

class User_car(BaseModel):
    id: int
    id_car: int
    id_user: int