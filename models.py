from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    name: str
    email: str


class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class Goal(BaseModel):
    goal: str
    daily: str
    day_Time: str
    process: str
