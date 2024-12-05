from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    name: str
    email: str


class Task(BaseModel):
    user_id: str
    title: str
    implementation_date: str
    description: Optional[str] = None
    completed: bool = False


class Goal(BaseModel):
    goal: str
    duration: str
    daily_time: str
    level: str
    approach: str
    user_id: str
