"""
A single saved meeting reminder shown below the meeting form.
"""
from bson import ObjectId
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from app.utils.datetime_utils import format_meeting_when


class MeetingCard(QWidget):
    delete_requested = Signal(ObjectId)

    def __init__(self, meeting: dict, parent=None):
        super().__init__(parent)
        self.meeting_id = meeting["_id"]

        self.setObjectName("MeetingCard")
        self.setMinimumHeight(60)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 12, 10)
        layout.setSpacing(12)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)

        when_text = format_meeting_when(meeting["meeting_time"])
        date_text = meeting["meeting_time"].strftime("%Y-%m-%d")
        time_label = QLabel(f"{when_text}  ·  {date_text}")
        time_label.setObjectName("MutedLabel")

        title_label = QLabel(meeting["title"])
        title_label.setObjectName("TaskName")
        title_label.setWordWrap(True)

        reminder_label = QLabel(f"Reminds {meeting['reminder_minutes']} min before")
        reminder_label.setObjectName("MutedLabel")

        text_col.addWidget(time_label)
        text_col.addWidget(title_label)
        text_col.addWidget(reminder_label)
        layout.addLayout(text_col, 1)

        self.delete_btn = QPushButton("✕")
        self.delete_btn.setObjectName("IconDeleteButton")
        self.delete_btn.setFixedSize(30, 30)
        self.delete_btn.setCursor(Qt.PointingHandCursor)
        self.delete_btn.setToolTip("Delete meeting")
        self.delete_btn.clicked.connect(
            lambda: self.delete_requested.emit(self.meeting_id)
        )
        layout.addWidget(self.delete_btn, 0, Qt.AlignTop)
