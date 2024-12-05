from typing import Dict, List
from fastapi import HTTPException
from pymongo.collection import Collection
from bson import ObjectId
from models import User, Task, Goal
from fastapi.encoders import jsonable_encoder


def str_to_objectid(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId")


def get_user(user_collection: Collection, goal_collection: Collection, user_id: str):
    try:
        user_object_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid User ID format")

    user = user_collection.find_one({"_id": user_object_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    goal = goal_collection.find_one({"user_id": user_id})
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    return {
        "name": user.get("name"),
        "email": user.get("email"),
        "goal": goal.get("goal"),
        "duration": goal.get("duration"),
        "daily_time": goal.get("daily_time"),
        "level": goal.get("level"),
        "approach": goal.get("approach"),
    }


def create_user(collection: Collection, user: User):
    result = collection.insert_one(user.dict())
    return {"message": "User created", "id": str(result.inserted_id)}


def update_user(collection: Collection, user_id: str, user: User):
    user_object_id = str_to_objectid(user_id)
    updated_data = user.dict()
    result = collection.update_one(
        {"_id": user_object_id}, {"$set": updated_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated"}


def delete_user(collection: Collection, user_id: str):
    user_object_id = str_to_objectid(user_id)
    result = collection.delete_one({"_id": user_object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}


def create_task(collection: Collection, task: Task):
    task_dict = task.dict()
    result = collection.insert_one(task_dict)
    task_dict["_id"] = str(result.inserted_id)
    return jsonable_encoder({"id": str(result.inserted_id), **task_dict})


def get_task(task_collection: Collection, user_id: str):
    tasks_cursor = task_collection.find({"user_id": user_id})
    tasks = list(tasks_cursor)
    if not tasks:
        raise HTTPException(status_code=404, detail="Goal not found")
    return [
        {
            "task_id": str(task["_id"]),
            "user_id": task.get("user_id"),
            "implementation_date": task.get("implementation_date"),
            "title": task.get("title"),
            "description": task.get("description"),
            "completed": task.get("completed"),
        }
        for task in tasks
    ]


def update_task(collection: Collection, task_id: str, task: Task):
    result = collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": task.dict(exclude_unset=True)}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": task_id, **task.dict()}


def delete_task(collection: Collection, task_id: str):
    result = collection.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}


def create_goal(collection: Collection, goal: Goal):
    goal_dict = goal.dict()
    result = collection.insert_one(goal_dict)
    goal_dict["_id"] = str(result.inserted_id)
    return jsonable_encoder({"id": str(result.inserted_id), **goal_dict})


def get_goal(collection: Collection, user_id: str) -> List[Dict]:
    goal = collection.find_one({"user_id": user_id})
    if goal is None:
        return []

    return [
        {
            "id": str(goal["_id"]),
            "goal": goal["goal"],
            "duration": goal["duration"],
            "daily_time": goal["daily_time"],
            "level": goal["level"],
            "approach": goal["approach"]
        }
    ]


def update_goal(collection: Collection, goal_id: str, goal: Goal):
    result = collection.update_one(
        {"_id": ObjectId(goal_id)},
        {"$set": goal.dict(exclude_unset=True)}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Goal not found")
    return {"id": goal_id, **goal.dict()}


def delete_goal(collection: Collection, goal_id: str):
    result = collection.delete_one({"_id": ObjectId(goal_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Goal not found")
    return {"message": "Goal deleted"}
