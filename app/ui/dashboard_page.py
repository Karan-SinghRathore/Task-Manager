"""
Dashboard page: add/list/complete/delete tasks, and a meeting reminder
card below the task list for scheduling meetings.
"""
from datetime import datetime

from bson import ObjectId
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDateEdit,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)

from app.core.meeting_service import MeetingService
from app.core.task_service import TaskService
from app.ui.animations import fade_in
from app.ui.widgets.empty_state import EmptyState
from app.ui.widgets.meeting_card import MeetingCard
from app.ui.widgets.task_card import TaskCard
from app.utils.datetime_utils import combine_date_time


class DashboardPage(QWidget):
    task_completed = Signal(dict)  # forwards the archived history entry

    def __init__(self, task_service: TaskService, meeting_service: MeetingService, parent=None):
        super().__init__(parent)
        self._task_service = task_service
        self._meeting_service = meeting_service
        self._selected_card = None

        self.setObjectName("PageContainer")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(32, 28, 32, 28)
        outer.setSpacing(20)

        title = QLabel("Dashboard")
        title.setObjectName("PageTitle")
        outer.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        outer.addWidget(scroll, 1)

        content = QWidget()
        scroll.setWidget(content)
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 4, 0)
        content_layout.setSpacing(20)

        content_layout.addWidget(self._build_add_task_card())
        content_layout.addWidget(self._build_task_list_card(), 1)
        content_layout.addWidget(self._build_meeting_card())
        content_layout.addStretch(0)

        self.refresh_tasks()
        self.refresh_meetings()

    # ---- Add task card ----

    def _build_add_task_card(self) -> QWidget:
        card = QFrame()
        card.setObjectName("SectionCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)

        heading = QLabel("Add Task")
        heading.setStyleSheet("font-size: 16px; font-weight: 600;")
        layout.addWidget(heading)

        row = QHBoxLayout()
        row.setSpacing(10)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("What do you need to do?")
        self.task_input.returnPressed.connect(self._on_add_task)
        row.addWidget(self.task_input, 1)

        add_btn = QPushButton("+")
        add_btn.setObjectName("AddButton")
        add_btn.setFixedSize(42, 42)
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setToolTip("Add task (Enter)")
        add_btn.clicked.connect(self._on_add_task)
        row.addWidget(add_btn)

        layout.addLayout(row)
        return card

    def _on_add_task(self) -> None:
        name = self.task_input.text()
        if not name.strip():
            return
        try:
            self._task_service.add_task(name)
        except Exception as exc:
            QMessageBox.warning(self, "Could not add task", str(exc))
            return
        self.task_input.clear()
        self.refresh_tasks()

    # ---- Task list card ----

    def _build_task_list_card(self) -> QWidget:
        card = QFrame()
        card.setObjectName("SectionCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)

        heading = QLabel("Tasks")
        heading.setStyleSheet("font-size: 16px; font-weight: 600;")
        layout.addWidget(heading)

        self.task_list_layout = QVBoxLayout()
        self.task_list_layout.setSpacing(8)
        layout.addLayout(self.task_list_layout)

        self._task_list_card = card
        return card

    def refresh_tasks(self) -> None:
        self._clear_layout(self.task_list_layout)
        tasks = self._task_service.list_tasks()

        if not tasks:
            empty = EmptyState(
                "✅",
                "No tasks yet",
                "Add your first task above to get started.",
            )
            self.task_list_layout.addWidget(empty)
            return

        self._selected_card = None
        for task in tasks:
            card = TaskCard(task)
            card.completed.connect(self._on_task_completed)
            card.delete_requested.connect(self._on_task_delete_requested)
            card.selected.connect(self._on_task_card_selected)
            self.task_list_layout.addWidget(card)
            fade_in(card)

    def _on_task_card_selected(self, card) -> None:
        if self._selected_card is not None and self._selected_card is not card:
            self._selected_card.set_selected(False)
        self._selected_card = card
        card.set_selected(True)

    def delete_selected_task(self) -> None:
        """Invoked by the main window's Delete key shortcut."""
        if self._selected_card is not None:
            self._on_task_delete_requested(self._selected_card.task_id)

    def _on_task_completed(self, task_id: ObjectId) -> None:
        try:
            entry = self._task_service.complete_task(task_id)
        except Exception as exc:
            QMessageBox.warning(self, "Could not complete task", str(exc))
            return
        self.refresh_tasks()
        if entry is not None:
            self.task_completed.emit(entry)

    def _on_task_delete_requested(self, task_id: ObjectId) -> None:
        confirm = QMessageBox.question(
            self,
            "Delete task",
            "Delete this task permanently? This cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return
        try:
            self._task_service.delete_task(task_id)
        except Exception as exc:
            QMessageBox.warning(self, "Could not delete task", str(exc))
            return
        self.refresh_tasks()

    # ---- Meeting reminder card ----

    def _build_meeting_card(self) -> QWidget:
        card = QFrame()
        card.setObjectName("SectionCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)

        heading = QLabel("Meeting Reminders")
        heading.setStyleSheet("font-size: 16px; font-weight: 600;")
        layout.addWidget(heading)

        self.meeting_title_input = QLineEdit()
        self.meeting_title_input.setPlaceholderText("Meeting title")
        layout.addWidget(self.meeting_title_input)

        form_row = QHBoxLayout()
        form_row.setSpacing(10)

        self.meeting_date_edit = QDateEdit()
        self.meeting_date_edit.setCalendarPopup(True)
        self.meeting_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.meeting_date_edit.setDate(datetime.now().date())
        form_row.addWidget(self.meeting_date_edit, 1)

        self.meeting_time_edit = QTimeEdit()
        self.meeting_time_edit.setDisplayFormat("hh:mm AP")
        now = datetime.now().time()
        self.meeting_time_edit.setTime(now)
        form_row.addWidget(self.meeting_time_edit, 1)

        reminder_label = QLabel("Remind (min):")
        reminder_label.setObjectName("MutedLabel")
        form_row.addWidget(reminder_label)

        self.reminder_minutes_spin = QSpinBox()
        self.reminder_minutes_spin.setRange(1, 180)
        self.reminder_minutes_spin.setValue(10)
        self.reminder_minutes_spin.setFixedWidth(70)
        form_row.addWidget(self.reminder_minutes_spin)

        layout.addLayout(form_row)

        save_btn = QPushButton("Save Meeting")
        save_btn.setObjectName("PrimaryButton")
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.clicked.connect(self._on_save_meeting)
        layout.addWidget(save_btn, 0, Qt.AlignRight)

        self.meeting_list_layout = QVBoxLayout()
        self.meeting_list_layout.setSpacing(8)
        layout.addLayout(self.meeting_list_layout)

        return card

    def _on_save_meeting(self) -> None:
        title = self.meeting_title_input.text()
        if not title.strip():
            QMessageBox.information(self, "Meeting title required", "Please enter a meeting title.")
            return

        meeting_dt = combine_date_time(
            self.meeting_date_edit.date(), self.meeting_time_edit.time()
        )
        reminder_minutes = self.reminder_minutes_spin.value()

        try:
            self._meeting_service.add_meeting(title, meeting_dt, reminder_minutes)
        except Exception as exc:
            QMessageBox.warning(self, "Could not save meeting", str(exc))
            return

        self.meeting_title_input.clear()
        self.refresh_meetings()

    def refresh_meetings(self) -> None:
        self._clear_layout(self.meeting_list_layout)
        meetings = self._meeting_service.list_meetings()

        if not meetings:
            empty = EmptyState(
                "\U0001F4C5",
                "No meetings scheduled",
                "Save a meeting above and we'll remind you before it starts.",
            )
            self.meeting_list_layout.addWidget(empty)
            return

        for meeting in meetings:
            card = MeetingCard(meeting)
            card.delete_requested.connect(self._on_meeting_delete_requested)
            self.meeting_list_layout.addWidget(card)
            fade_in(card)

    def _on_meeting_delete_requested(self, meeting_id: ObjectId) -> None:
        confirm = QMessageBox.question(
            self,
            "Delete meeting",
            "Delete this meeting reminder?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return
        try:
            self._meeting_service.delete_meeting(meeting_id)
        except Exception as exc:
            QMessageBox.warning(self, "Could not delete meeting", str(exc))
            return
        self.refresh_meetings()

    # ---- helpers ----

    @staticmethod
    def _clear_layout(layout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
