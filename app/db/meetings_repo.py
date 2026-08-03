"""
Data access for the `meetings` collection (scheduled meeting reminders).
"""
from datetime import datetime

from bson import ObjectId

from app.config import COLLECTION_MEETINGS, DEFAULT_REMINDER_MINUTES


class MeetingsRepository:
    def __init__(self, connection):
        self._connection = connection

    @property
    def _collection(self):
        return self._connection.db[COLLECTION_MEETINGS]

    def add_meeting(
        self,
        title: str,
        meeting_dt: datetime,
        reminder_minutes: int = DEFAULT_REMINDER_MINUTES,
    ) -> dict:
        doc = {
            "title": title,
            "meeting_time": meeting_dt,
            "reminder_minutes": reminder_minutes,
            "notified": False,
            "created_at": datetime.now(),
        }
        result = self._collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    def get_all(self) -> list[dict]:
        """Soonest meeting first."""
        return list(self._collection.find().sort("meeting_time", 1))

    def get_pending_unnotified(self) -> list[dict]:
        return list(self._collection.find({"notified": False}))

    def mark_notified(self, meeting_id: ObjectId) -> None:
        self._collection.update_one(
            {"_id": meeting_id}, {"$set": {"notified": True}}
        )

    def delete_meeting(self, meeting_id: ObjectId) -> None:
        self._collection.delete_one({"_id": meeting_id})
