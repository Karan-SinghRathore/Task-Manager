"""
Business logic for meeting reminders: creating meetings and finding
meetings that are due for a notification.
"""
from datetime import datetime, timedelta

from bson import ObjectId

from app.config import DEFAULT_REMINDER_MINUTES
from app.db.repositories import Repositories


class MeetingService:
    def __init__(self, repos: Repositories):
        self._repos = repos

    def list_meetings(self) -> list[dict]:
        return self._repos.meetings.get_all()

    def add_meeting(
        self,
        title: str,
        meeting_dt: datetime,
        reminder_minutes: int = DEFAULT_REMINDER_MINUTES,
    ) -> dict | None:
        title = title.strip()
        if not title:
            return None
        return self._repos.meetings.add_meeting(title, meeting_dt, reminder_minutes)

    def delete_meeting(self, meeting_id: ObjectId) -> None:
        self._repos.meetings.delete_meeting(meeting_id)

    def find_due_meetings(self) -> list[dict]:
        """Meetings whose reminder window has been reached but that have
        not yet been notified about. A meeting becomes due once
        (meeting_time - reminder_minutes) <= now < meeting_time.
        """
        now = datetime.now()
        due = []
        for meeting in self._repos.meetings.get_pending_unnotified():
            reminder_at = meeting["meeting_time"] - timedelta(
                minutes=meeting["reminder_minutes"]
            )
            if reminder_at <= now < meeting["meeting_time"]:
                due.append(meeting)
        return due

    def mark_notified(self, meeting_id: ObjectId) -> None:
        self._repos.meetings.mark_notified(meeting_id)
