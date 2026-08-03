"""
MongoDB connection management. Connects to a local MongoDB instance and
exposes the task_manager database. Never raises on import/connect failure -
callers should check `is_connected` and surface a friendly message.
"""
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from app.config import DB_NAME, MONGO_SERVER_TIMEOUT_MS, MONGO_URI


class MongoConnection:
    """Lazily connects to MongoDB and caches the client/database handles."""

    def __init__(self):
        self._client: MongoClient | None = None
        self._db = None
        self._error: str | None = None

    def connect(self) -> bool:
        """Attempt to connect and verify the server is reachable.

        Returns True on success, False otherwise. The failure reason is
        available via `last_error`.
        """
        try:
            self._client = MongoClient(
                MONGO_URI,
                serverSelectionTimeoutMS=MONGO_SERVER_TIMEOUT_MS,
            )
            # Force a round-trip so unreachable servers fail fast, here,
            # rather than on the first real query later.
            self._client.admin.command("ping")
            self._db = self._client[DB_NAME]
            self._error = None
            return True
        except PyMongoError as exc:
            self._error = str(exc)
            self._client = None
            self._db = None
            return False

    @property
    def is_connected(self) -> bool:
        return self._db is not None

    @property
    def db(self):
        return self._db

    @property
    def last_error(self) -> str | None:
        return self._error

    def close(self):
        if self._client is not None:
            self._client.close()
            self._client = None
            self._db = None


# Single shared connection instance for the whole app.
mongo_connection = MongoConnection()
