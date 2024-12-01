from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    name: str
    email: str
    goal: str
    daily: str
    day_Time: str
    process: str


class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
