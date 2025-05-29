from pydantic import BaseModel
from typing import List

class JobCreate(BaseModel):
    title: str
    description: str
    employment_type: str
    locations: List[str]
    category: str
    salary: str
    company_name: str