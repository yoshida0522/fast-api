from fastapi import FastAPI
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from models import User, Task
import crud

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["API_DB"]
user_collection = db["user"]
task_collection = db["task"]

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Fast API"}


@app.get("/users")
async def get_users():
    return crud.get_users(user_collection)


@app.post("/users")
async def create_user(user: User):
    return crud.create_user(user_collection, user)


@app.put("/users/{user_id}")
async def update_user(user_id: str, user: User):
    return crud.update_user(user_collection, user_id, user)


@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    return crud.delete_user(user_collection, user_id)


@app.get("/tasks")
async def get_tasks():
    return crud.get_tasks(task_collection)


@app.post("/tasks")
async def create_task(task: Task):
    return crud.create_task(task_collection, task)


@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task: Task):
    return crud.update_task(task_collection, task_id, task)


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    return crud.delete_task(task_collection, task_id)
