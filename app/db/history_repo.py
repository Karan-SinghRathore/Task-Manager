"""
Data access for the `history` collection (archived completed/pending-closed tasks).
"""
from datetime import datetime

from bson import ObjectId

from app.config import COLLECTION_HISTORY


class HistoryRepository:
    def __init__(self, connection):
        self._connection = connection

    @property
    def _collection(self):
        return self._connection.db[COLLECTION_HISTORY]

    def add_entry(self, name: str, status: str, when: datetime) -> dict:
        doc = {
            "name": name,
            "status": status,
            "date": when.strftime("%Y-%m-%d"),
            "time": when.strftime("%I:%M %p"),
            "archived_at": when,
        }
        result = self._collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    def get_all(self) -> list[dict]:
        """Newest first."""
        return list(self._collection.find().sort("archived_at", -1))

    def delete_entry(self, entry_id: ObjectId) -> None:
        self._collection.delete_one({"_id": entry_id})

    def clear_all(self) -> None:
        self._collection.delete_many({})
