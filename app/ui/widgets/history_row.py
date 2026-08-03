"""
A single archived task row shown on the History page.
"""
from bson import ObjectId
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from app.config import STATUS_COMPLETED


class HistoryRow(QWidget):
    delete_requested = Signal(ObjectId)

    def __init__(self, entry: dict, parent=None):
        super().__init__(parent)
        self.entry_id = entry["_id"]

        self.setObjectName("HistoryRow")
        self.setMinimumHeight(56)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 12, 10)
        layout.setSpacing(14)

        name_label = QLabel(entry["name"])
        name_label.setObjectName("TaskName")
        name_label.setWordWrap(True)
        layout.addWidget(name_label, 1)

        is_completed = entry["status"] == STATUS_COMPLETED
        status_label = QLabel(entry["status"])
        status_label.setObjectName(
            "StatusPillCompleted" if is_completed else "StatusPillPending"
        )
        layout.addWidget(status_label, 0, Qt.AlignVCenter)

        date_col = QVBoxLayout()
        date_col.setSpacing(0)
        date_label = QLabel(entry["date"])
        date_label.setObjectName("MutedLabel")
        time_label = QLabel(entry["time"])
        time_label.setObjectName("MutedLabel")
        date_col.addWidget(date_label)
        date_col.addWidget(time_label)
        date_wrap = QWidget()
        date_wrap.setLayout(date_col)
        date_wrap.setFixedWidth(90)
        layout.addWidget(date_wrap)

        self.delete_btn = QPushButton("✕")
        self.delete_btn.setObjectName("IconDeleteButton")
        self.delete_btn.setFixedSize(30, 30)
        self.delete_btn.setCursor(Qt.PointingHandCursor)
        self.delete_btn.setToolTip("Delete entry")
        self.delete_btn.clicked.connect(
            lambda: self.delete_requested.emit(self.entry_id)
        )
        layout.addWidget(self.delete_btn)
