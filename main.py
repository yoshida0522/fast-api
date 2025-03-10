from typing import List
from fastapi import Body, FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from models import Graph, GraphData, User, Task, Goal
import crud

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DIFY_API_KEY = os.getenv("DIFY_API_KEY")

client = MongoClient(MONGO_URI)
db = client["API_DB"]
user_collection = db["user"]
task_collection = db["task"]
goal_collection = db["goal"]
graph_collection = db["graph"]

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3000/goals",
    "https://python-port.vercel.app",
    "https://fast-api-sandy.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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


@app.get("/tasks")
async def get_task(user_id: str):
    return crud.get_task(task_collection, user_id)


@app.get("/tasks/{user_id}")
def get_task(user_id: str):
    tasks = list(task_collection.find(
        {"user_id": user_id}, {"_id": 0, "completed": 1, "implementation_date": 1}))
    return tasks


@app.post("/save-tasks/")
async def create_task(tasks: List[Task]):
    if not tasks:
        raise HTTPException(
            status_code=400, detail="タスクリストが空です。正しいデータを送信してください。")
    try:
        result = crud.create_task(task_collection, tasks)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"タスク保存中にエラーが発生しました: {str(e)}")


@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task: Task):
    return crud.update_task(task_collection, task_id, task)


@app.delete("/all-tasks/{user_id}")
async def delete_task(user_id: str):
    return crud.delete_task(task_collection, user_id)


@app.get("/goals/{user_id}")
async def get_goal(user_id: str):
    return crud.get_goal(goal_collection, user_id)


@app.post("/goals/{user_id}")
async def create_goal(user_id: str = Path(...), goal: Goal = Body(...)):
    try:
        goal_dict = goal.dict()
        goal_dict["user_id"] = user_id
        result = goal_collection.insert_one(goal_dict)
        return {"message": "Goal created with user_id", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(
            status_code=422, detail=f"Error creating goal: {str(e)}")


@app.put("/goals/{user_id}")
async def update_goal(user_id: str, goal: Goal):
    return crud.update_goal(goal_collection, user_id, goal)


@app.delete("/goals/{user_id}")
async def delete_goal(user_id: str):
    return crud.delete_goal(goal_collection, user_id)


@app.get("/graph/{user_id}", response_model=List[Graph])
async def get_graph_data(user_id: str):
    data = crud.get_graph(user_id, graph_collection)
    if not data:
        return []
    return data


@app.post("/graph/{user_id}")
async def create_graph(user_id: str, report: GraphData):
    try:
        return crud.create_graph(graph_collection, user_id, report.filteredTasks, report.total_task, report.completed_task, report.completion_rate)
    except Exception as e:
        print(f"Error in update_graph: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to save progress report: {str(e)}")


@app.delete("/graph/{user_id}")
async def delete_graph_data(user_id: str):
    return crud.delete_graph_data(user_id, graph_collection)
