"""
Data access for the `tasks` collection (pending dashboard tasks).
"""
from datetime import datetime

from bson import ObjectId

from app.config import COLLECTION_TASKS


class TasksRepository:
    def __init__(self, connection):
        self._connection = connection

    @property
    def _collection(self):
        return self._connection.db[COLLECTION_TASKS]

    def add_task(self, name: str) -> dict:
        doc = {"name": name, "created_at": datetime.now()}
        result = self._collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    def get_all_tasks(self) -> list[dict]:
        return list(self._collection.find().sort("created_at", 1))

    def delete_task(self, task_id: ObjectId) -> None:
        self._collection.delete_one({"_id": task_id})

    def get_task(self, task_id: ObjectId) -> dict | None:
        return self._collection.find_one({"_id": task_id})

    def delete_all(self) -> None:
        self._collection.delete_many({})
