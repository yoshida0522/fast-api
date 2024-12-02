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


def get_users(collection: Collection):
    users = collection.find()
    user_list = []
    for user in users:
        user["_id"] = str(user["_id"])
        user_list.append(user)
    return user_list


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


def get_tasks(collection: Collection):
    tasks = collection.find()
    return [{"id": str(task["_id"]), "title": task["title"], "description": task.get("description", ""), "completed": task["completed"]} for task in tasks]


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


def get_goals(collection: Collection):
    goals = collection.find()
    return [{"id": str(goal["_id"]), "daily": goal["daily"], "day_Time": goal.get("day_Time", ""), "process": goal["process"]} for goal in goals]


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
