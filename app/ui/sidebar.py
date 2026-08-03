"""
Left navigation panel with Dashboard / History entries.
"""
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QButtonGroup, QLabel, QPushButton, QVBoxLayout, QWidget

from app.config import APP_NAME


class Sidebar(QWidget):
    navigate = Signal(str)  # emits "dashboard" or "history"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(220)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        title = QLabel(APP_NAME)
        title.setObjectName("SidebarTitle")
        layout.addWidget(title)

        self._group = QButtonGroup(self)
        self._group.setExclusive(True)

        self.dashboard_btn = self._make_nav_button("  \U0001F4CB   Dashboard")
        self.history_btn = self._make_nav_button("  \U0001F553   History")

        layout.addWidget(self.dashboard_btn)
        layout.addWidget(self.history_btn)
        layout.addStretch(1)

        self.dashboard_btn.setChecked(True)
        self.dashboard_btn.clicked.connect(lambda: self.navigate.emit("dashboard"))
        self.history_btn.clicked.connect(lambda: self.navigate.emit("history"))

    def _make_nav_button(self, text: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setObjectName("NavButton")
        btn.setCheckable(True)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(44)
        self._group.addButton(btn)
        margin = 12
        btn.setStyleSheet(f"margin-left: {margin}px; margin-right: {margin}px;")
        return btn
