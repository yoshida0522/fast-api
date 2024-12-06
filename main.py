from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from models import User, Task, Goal
import crud

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DIFY_API_KEY = os.getenv("DIFY_API_KEY")

client = MongoClient(MONGO_URI)
db = client["API_DB"]
user_collection = db["user"]
task_collection = db["task"]
goal_collection = db["goal"]

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3000/goals",
    "https://fast-api-sandy.vercel.app/",  # 本番環境のURL
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],  # 全てのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Fast API"}


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    try:
        return crud.get_user(user_collection, goal_collection, user_id)
    except HTTPException as e:
        return {"error": e.detail}


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
async def get_task(user_id: str):
    return crud.get_task(task_collection, user_id)


@app.post("/tasks")
async def create_task(task: Task):
    return crud.create_task(task_collection, task)


@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task: Task):
    return crud.update_task(task_collection, task_id, task)


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    return crud.delete_task(task_collection, task_id)


@app.get("/goals/{user_id}")
async def get_goal(user_id: str):
    return crud.get_goal(goal_collection, user_id)


# @app.post("/goals")
# async def create_goal_with_user_id(goal: Goal, user_id: str = Query(...)):
#     goal_dict = goal.dict()
#     goal_dict["user_id"] = user_id
#     goal_collection.insert_one(goal_dict)
#     return {"message": "Goal created with user_id"}
@app.post("/goals/{user_id}")
# async def create_goal(goal: Goal, user_id: str = Query(...)):
async def create_goal(goal: Goal, user_id: str = Path(...)):
    goal_dict = goal.dict()
    goal_dict["user_id"] = user_id
    goal_collection.insert_one(goal_dict)
    return {"message": "Goal created with user_id"}


# @app.put("/goals/{goal_id}")
# async def update_goal(goal_id: str, goal: Goal):
#     return crud.update_goal(goal_collection, goal_id, goal)
@app.put("/goals/{user_id}")
async def update_goal(user_id: str, goal: Goal):
    return crud.update_goal(goal_collection, user_id, goal)


@app.delete("/goals/{goal_id}")
async def delete_goal(goal_id: str):
    return crud.delete_goal(goal_collection, goal_id)
