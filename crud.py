from typing import Dict, List
from fastapi import HTTPException
from pymongo.collection import Collection
from bson import ObjectId
from models import Graph,  User, Task, Goal
from fastapi.encoders import jsonable_encoder


def str_to_objectid(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId")


def get_user(user_collection: Collection, goal_collection: Collection, user_id: str):
    user = user_collection.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    goal = goal_collection.find_one({"user_id": user_id})

    if goal:
        return {
            "name": user.get("name"),
            "email": user.get("email"),
            "user_id": user.get("user_id"),
            "goal": goal.get("goal"),
            "duration": goal.get("duration"),
            "daily_time": goal.get("daily_time"),
            "level": goal.get("level"),
            "approach": goal.get("approach"),
        }
    else:
        return {
            "name": user.get("name"),
            "email": user.get("email"),
            "user_id": user.get("user_id"),
            "goal": "",
            "duration": "",
            "daily_time": "",
            "level": "",
            "approach": "",
        }


def create_user(collection: Collection, user: User):
    existing_user = collection.find_one(
        {"name": user.name, "email": user.email})

    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this name and email already exists.")

    user_dict = jsonable_encoder(user)
    result = collection.insert_one(user_dict)
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


def create_task(collection: Collection, tasks: List[Task]):
    try:
        if not tasks:
            raise ValueError("保存するタスクリストが空です。")
        task_dicts = [task.dict() for task in tasks]
        collection.insert_many(task_dicts)
        return {"message": "タスクが保存されました"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"サーバーエラー: {str(e)}")


def get_task(task_collection: Collection, user_id: str):
    tasks_cursor = task_collection.find({"user_id": user_id})
    tasks = list(tasks_cursor)
    if not tasks:
        return []
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
        print(f"Goal not found for user_id: {user_id}")
        return []

    return [
        {
            "id": str(goal["_id"]),
            "goal": goal["goal"],
            "duration": goal["duration"],
            "daily_time": goal["daily_time"],
            "level": goal["level"],
            "approach": goal["approach"],
            "user_id": goal["user_id"],
            "date": goal["date"]
        }
    ]


def update_goal(collection: Collection, user_id: str, goal: Goal):
    result = collection.update_one(
        {"user_id": user_id},
        {"$set": goal.dict(exclude_unset=True)}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Goal not found")
    return {"user_id": user_id, **goal.dict()}


def delete_goal(collection: Collection, goal_id: str):
    result = collection.delete_one({"_id": ObjectId(goal_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Goal not found")
    return {"message": "Goal deleted"}


def get_graph(user_id: str, graph_collection: Collection) -> List[Graph]:
    try:
        results = graph_collection.find(
            {"user_id": user_id}, {"_id": 0, "task_date": 1, "completion_rate": 1}
        )
        data = [Graph(**result) for result in results]
        return data
    except Exception as e:
        raise Exception(f"Error fetching graph data: {str(e)}")


def create_graph(collection: Collection, user_id: str, filteredTasks: list, totalTasks: int, completedTasks: int, completionRate: float):
    if not filteredTasks:
        raise ValueError("Filtered tasks cannot be empty.")
    if not isinstance(completionRate, float):
        raise ValueError("Completion rate must be a float.")
    if not isinstance(totalTasks, int) or not isinstance(completedTasks, int):
        raise ValueError("Total tasks and completed tasks must be integers.")

    new_data = {
        "user_id": user_id,
        "task_date": filteredTasks[0]["implementation_date"],
        "total_task": totalTasks,
        "completed_task": completedTasks,
        "completion_rate": completionRate,
        "tasks": filteredTasks,
    }

    result = collection.insert_one(new_data)

    if not result.acknowledged:
        raise HTTPException(
            status_code=500, detail="Failed to insert graph data"
        )

    inserted_graph = collection.find_one({"_id": result.inserted_id})

    return {
        "user_id": inserted_graph["user_id"],
        "task_date": inserted_graph["task_date"],
        "total_task": inserted_graph["total_task"],
        "completed_task": inserted_graph["completed_task"],
        "completion_rate": inserted_graph["completion_rate"]
    }


def delete_graph_data(user_id, graph_collection):
    result = graph_collection.delete_many({"user_id": user_id})
    if result.deleted_count > 0:
        return {"message": "Graphデータの削除が成功しました"}
    return
