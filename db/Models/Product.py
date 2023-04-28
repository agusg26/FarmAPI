from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    id: Optional[str]
    name: str
    price: int
    stock: int
    last_update: Optional[str]