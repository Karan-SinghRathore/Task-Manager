"""
Central access point for all repositories, built on top of the shared
MongoConnection instance.
"""
from app.db.connection import mongo_connection
from app.db.history_repo import HistoryRepository
from app.db.meetings_repo import MeetingsRepository
from app.db.tasks_repo import TasksRepository


class Repositories:
    def __init__(self, connection):
        self.tasks = TasksRepository(connection)
        self.history = HistoryRepository(connection)
        self.meetings = MeetingsRepository(connection)


repositories = Repositories(mongo_connection)
