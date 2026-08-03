"""
Polls MongoDB on a QTimer for meetings that are due for a reminder and
fires a toast notification exactly once per meeting.
"""
import logging

from PySide6.QtCore import QObject, QTimer, Signal

from app.config import MEETING_POLL_INTERVAL_MS
from app.core.meeting_service import MeetingService
from app.notifications.toast import toast_notifier

logger = logging.getLogger(__name__)


class MeetingMonitor(QObject):
    """Runs on the Qt main thread; each tick does a fast local Mongo query."""

    meeting_notified = Signal(str)  # emits meeting title after notifying

    def __init__(self, meeting_service: MeetingService, parent=None):
        super().__init__(parent)
        self._meeting_service = meeting_service
        self._timer = QTimer(self)
        self._timer.setInterval(MEETING_POLL_INTERVAL_MS)
        self._timer.timeout.connect(self._check_due_meetings)

    def start(self) -> None:
        self._check_due_meetings()
        self._timer.start()

    def stop(self) -> None:
        self._timer.stop()

    def _check_due_meetings(self) -> None:
        try:
            due_meetings = self._meeting_service.find_due_meetings()
        except Exception as exc:
            logger.warning("Meeting monitor query failed: %s", exc)
            return

        for meeting in due_meetings:
            minutes = meeting["reminder_minutes"]
            toast_notifier.show(
                "Meeting Reminder",
                f"{meeting['title']} starts in {minutes} minutes.",
            )
            self._meeting_service.mark_notified(meeting["_id"])
            self.meeting_notified.emit(meeting["title"])
