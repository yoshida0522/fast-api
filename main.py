from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware  # CORS ミドルウェアのインポート
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from models import User, Task, Goal, WorkflowInput
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

# CORS ミドルウェアの設定
origins = [
    "http://localhost:3000",
    "http://localhost:3000/goals",
    "https://fast-api-sandy.vercel.app/",  # 本番環境のURL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 許可するオリジン
    allow_credentials=True,  # Cookie を許可する場合
    allow_methods=["*"],  # 許可する HTTP メソッド
    allow_headers=["*"],  # 許可する HTTP ヘッダー
)


@app.get("/")
async def root():
    return {"message": "Fast API"}


# @app.get("/users")
# async def get_users():
#     return crud.get_users(user_collection)
@app.get("/user/{user_id}")
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
async def get_task():
    return crud.get_task(task_collection)


@app.post("/tasks")
async def create_task(task: Task):
    return crud.create_task(task_collection, task)


@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task: Task):
    return crud.update_task(task_collection, task_id, task)


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    return crud.delete_task(task_collection, task_id)


# @app.get("/goals")
# async def get_goals():
#     return crud.get_goals(goal_collection)


# @app.post("/goals")
# async def create_goal(goal: Goal):
#     return crud.create_goal(goal_collection, goal)
@app.post("/goals")
async def create_goal_with_user_id(goal: Goal, user_id: str = Query(...)):
    goal_dict = goal.dict()
    goal_dict["user_id"] = user_id
    goal_collection.insert_one(goal_dict)
    return {"message": "Goal created with user_id"}


@app.put("/goals/{goal_id}")
async def update_goal(goal_id: str, goal: Goal):
    return crud.update_goal(goal_collection, goal_id, goal)


@app.delete("/goals/{goal_id}")
async def delete_goal(goal_id: str):
    return crud.delete_goal(goal_collection, goal_id)
