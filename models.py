from pydantic import BaseModel
from typing import List, Optional


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


class GraphData(BaseModel):
    task_date: str
    total_task: int
    completed_task: int
    completion_rate: float
    user_id: str
    filteredTasks: List[dict]


class Graph(BaseModel):
    task_date: str
    completion_rate: float
