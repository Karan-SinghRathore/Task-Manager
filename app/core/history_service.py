"""
Business logic for the History page: listing, searching, deleting entries.
"""
from bson import ObjectId

from app.db.repositories import Repositories


class HistoryService:
    def __init__(self, repos: Repositories):
        self._repos = repos

    def list_all(self) -> list[dict]:
        """Already sorted newest-first by the repository."""
        return self._repos.history.get_all()

    def search(self, query: str) -> list[dict]:
        entries = self.list_all()
        query = query.strip().lower()
        if not query:
            return entries
        return [e for e in entries if query in e["name"].lower()]

    def delete_entry(self, entry_id: ObjectId) -> None:
        self._repos.history.delete_entry(entry_id)

    def clear_all(self) -> None:
        self._repos.history.clear_all()
