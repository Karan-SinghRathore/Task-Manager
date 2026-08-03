"""
Business logic for tasks: creating, completing, deleting, and archiving
pending tasks into history (used both by manual checkbox completion and
by the on-close archival sweep).
"""
from datetime import datetime

from bson import ObjectId

from app.config import STATUS_COMPLETED, STATUS_PENDING
from app.db.repositories import Repositories


class TaskService:
    def __init__(self, repos: Repositories):
        self._repos = repos

    def list_tasks(self) -> list[dict]:
        return self._repos.tasks.get_all_tasks()

    def add_task(self, name: str) -> dict | None:
        name = name.strip()
        if not name:
            return None
        return self._repos.tasks.add_task(name)

    def delete_task(self, task_id: ObjectId) -> None:
        self._repos.tasks.delete_task(task_id)

    def complete_task(self, task_id: ObjectId) -> dict | None:
        """Move a task from the dashboard to history as Completed."""
        task = self._repos.tasks.get_task(task_id)
        if task is None:
            return None
        entry = self._repos.history.add_entry(
            name=task["name"], status=STATUS_COMPLETED, when=datetime.now()
        )
        self._repos.tasks.delete_task(task_id)
        return entry

    def archive_all_pending_on_close(self) -> int:
        """Move every remaining dashboard task into history as Pending.

        Called when the application is closing. Returns the number of
        tasks archived.
        """
        pending_tasks = self._repos.tasks.get_all_tasks()
        closed_at = datetime.now()
        for task in pending_tasks:
            self._repos.history.add_entry(
                name=task["name"], status=STATUS_PENDING, when=closed_at
            )
            self._repos.tasks.delete_task(task["_id"])
        return len(pending_tasks)
