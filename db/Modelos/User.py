from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[str]
    fullname: str
    email: str
    disabled = True
