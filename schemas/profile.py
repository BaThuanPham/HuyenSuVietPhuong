from pydantic import BaseModel
from typing import Optional

class ProfileCreate(BaseModel):
    phone: str
    education: str
    experience: str
    skills: str


class ProfileUpdate(BaseModel):
    full_name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    education: Optional[str]
    experience: Optional[str]
    skills: Optional[str]
