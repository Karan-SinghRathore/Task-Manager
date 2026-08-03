"""
History page: search, list, delete individual entries, and clear all
archived tasks (both Completed and Pending-on-close).
"""
from bson import ObjectId
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.core.history_service import HistoryService
from app.ui.animations import fade_in
from app.ui.widgets.empty_state import EmptyState
from app.ui.widgets.history_row import HistoryRow


class HistoryPage(QWidget):
    def __init__(self, history_service: HistoryService, parent=None):
        super().__init__(parent)
        self._history_service = history_service

        self.setObjectName("PageContainer")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(32, 28, 32, 28)
        outer.setSpacing(18)

        header_row = QHBoxLayout()
        title = QLabel("History")
        title.setObjectName("PageTitle")
        header_row.addWidget(title)
        header_row.addStretch(1)

        clear_btn = QPushButton("Clear History")
        clear_btn.setObjectName("DangerButton")
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.clicked.connect(self._on_clear_history)
        header_row.addWidget(clear_btn)
        outer.addLayout(header_row)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search history by task name...")
        self.search_input.textChanged.connect(self.refresh)
        outer.addWidget(self.search_input)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        outer.addWidget(scroll, 1)

        content = QWidget()
        scroll.setWidget(content)
        self.list_layout = QVBoxLayout(content)
        self.list_layout.setContentsMargins(0, 0, 4, 0)
        self.list_layout.setSpacing(8)

        self.refresh()

    def refresh(self) -> None:
        self._clear_layout(self.list_layout)
        query = self.search_input.text()
        entries = self._history_service.search(query)

        if not entries:
            message = (
                "No history yet"
                if not query.strip()
                else "No matching results"
            )
            subtitle = (
                "Completed and closed-pending tasks will appear here."
                if not query.strip()
                else "Try a different search term."
            )
            empty = EmptyState("\U0001F553", message, subtitle)
            self.list_layout.addWidget(empty)
            return

        for entry in entries:
            row = HistoryRow(entry)
            row.delete_requested.connect(self._on_delete_entry)
            self.list_layout.addWidget(row)
            fade_in(row)

    def _on_delete_entry(self, entry_id: ObjectId) -> None:
        confirm = QMessageBox.question(
            self,
            "Delete entry",
            "Delete this history entry permanently?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return
        try:
            self._history_service.delete_entry(entry_id)
        except Exception as exc:
            QMessageBox.warning(self, "Could not delete entry", str(exc))
            return
        self.refresh()

    def _on_clear_history(self) -> None:
        confirm = QMessageBox.question(
            self,
            "Clear history",
            "Delete every history record permanently? This cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return
        try:
            self._history_service.clear_all()
        except Exception as exc:
            QMessageBox.warning(self, "Could not clear history", str(exc))
            return
        self.refresh()

    @staticmethod
    def _clear_layout(layout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
