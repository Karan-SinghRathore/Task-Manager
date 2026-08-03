"""
Task Manager - entry point.

Connects to local MongoDB, then launches the PySide6 desktop UI. If
MongoDB is not reachable, shows a friendly dialog instead of crashing.
"""
import logging
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox

from app.config import APP_NAME, ICON_PATH
from app.core.history_service import HistoryService
from app.core.meeting_service import MeetingService
from app.core.task_service import TaskService
from app.db.connection import mongo_connection
from app.db.repositories import repositories
from app.ui.main_window import MainWindow
from app.ui.theme import STYLESHEET

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setStyleSheet(STYLESHEET)
    if ICON_PATH.exists():
        app.setWindowIcon(QIcon(str(ICON_PATH)))

    if not mongo_connection.connect():
        QMessageBox.critical(
            None,
            APP_NAME,
            "MongoDB is not running. Please start the MongoDB service.",
        )
        return 1

    task_service = TaskService(repositories)
    history_service = HistoryService(repositories)
    meeting_service = MeetingService(repositories)

    window = MainWindow(task_service, history_service, meeting_service)
    window.show()

    exit_code = app.exec()
    mongo_connection.close()
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
