"""
A single task row shown on the Dashboard: checkbox + name + delete button.
Clicking anywhere on the row (outside the checkbox/delete button) selects
it, so the Delete key can remove the currently selected task.
"""
from bson import ObjectId
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QPushButton, QWidget


class TaskCard(QWidget):
    completed = Signal(ObjectId)
    delete_requested = Signal(ObjectId)
    selected = Signal(object)  # emits self

    def __init__(self, task: dict, parent=None):
        super().__init__(parent)
        self.task_id = task["_id"]
        self.task_name = task["name"]
        self._is_selected = False

        self.setObjectName("TaskCard")
        self.setMinimumHeight(56)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 12, 10)
        layout.setSpacing(12)

        self.checkbox = QCheckBox()
        self.checkbox.setCursor(Qt.PointingHandCursor)
        self.checkbox.stateChanged.connect(self._on_checked)
        layout.addWidget(self.checkbox)

        self.name_label = QLabel(self.task_name)
        self.name_label.setObjectName("TaskName")
        self.name_label.setWordWrap(True)
        layout.addWidget(self.name_label, 1)

        self.delete_btn = QPushButton("✕")
        self.delete_btn.setObjectName("IconDeleteButton")
        self.delete_btn.setFixedSize(30, 30)
        self.delete_btn.setCursor(Qt.PointingHandCursor)
        self.delete_btn.setToolTip("Delete task")
        self.delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.task_id))
        layout.addWidget(self.delete_btn)

    def _on_checked(self, state) -> None:
        if state == Qt.Checked.value or state == 2:
            self.completed.emit(self.task_id)

    def mousePressEvent(self, event) -> None:
        self.selected.emit(self)
        super().mousePressEvent(event)

    def set_selected(self, is_selected: bool) -> None:
        self._is_selected = is_selected
        border_color = "#4da3ff" if is_selected else "transparent"
        self.setStyleSheet(f"#TaskCard {{ border: 1px solid {border_color}; }}" if is_selected else "")
