"""
Main application window: hosts the sidebar + page stack, the system tray
icon, global keyboard shortcuts, and window geometry persistence.

Close (X) behavior: always archives pending tasks to history and quits
the application immediately. A separate "Minimize to Tray" action (menu
bar or the window's minimize button override) hides the window to the
tray instead, keeping the meeting monitor running in the background.
"""
import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QMainWindow,
    QMenu,
    QMessageBox,
    QStackedWidget,
    QSystemTrayIcon,
    QWidget,
)

from PySide6.QtWidgets import QHBoxLayout

from app.config import APP_NAME, ICON_PATH
from app.core.history_service import HistoryService
from app.core.meeting_service import MeetingService
from app.core.task_service import TaskService
from app.notifications.meeting_monitor import MeetingMonitor
from app.ui.dashboard_page import DashboardPage
from app.ui.history_page import HistoryPage
from app.ui.sidebar import Sidebar
from app.utils.settings import AppSettings

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(
        self,
        task_service: TaskService,
        history_service: HistoryService,
        meeting_service: MeetingService,
        parent=None,
    ):
        super().__init__(parent)
        self._task_service = task_service
        self._history_service = history_service
        self._meeting_service = meeting_service
        self._app_settings = AppSettings()
        self._is_quitting = False

        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(900, 640)
        if ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(ICON_PATH)))

        self._build_ui()
        self._build_tray_icon()
        self._build_shortcuts()
        self._restore_geometry()

        self._meeting_monitor = MeetingMonitor(self._meeting_service, self)
        self._meeting_monitor.meeting_notified.connect(self._on_meeting_notified)
        self._meeting_monitor.start()

    # ---- UI construction ----

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.sidebar.navigate.connect(self._on_navigate)
        layout.addWidget(self.sidebar)

        self.pages = QStackedWidget()
        layout.addWidget(self.pages, 1)

        self.dashboard_page = DashboardPage(self._task_service, self._meeting_service)
        self.history_page = HistoryPage(self._history_service)

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.history_page)
        self.pages.setCurrentWidget(self.dashboard_page)

    def _on_navigate(self, key: str) -> None:
        if key == "dashboard":
            self.dashboard_page.refresh_tasks()
            self.dashboard_page.refresh_meetings()
            self.pages.setCurrentWidget(self.dashboard_page)
        elif key == "history":
            self.history_page.refresh()
            self.pages.setCurrentWidget(self.history_page)

    # ---- Tray icon ----

    def _build_tray_icon(self) -> None:
        self.tray_icon = QSystemTrayIcon(self)
        if ICON_PATH.exists():
            self.tray_icon.setIcon(QIcon(str(ICON_PATH)))
        self.tray_icon.setToolTip(APP_NAME)

        menu = QMenu()
        restore_action = menu.addAction("Open Task Manager")
        restore_action.triggered.connect(self._restore_from_tray)
        menu.addSeparator()
        minimize_action = menu.addAction("Minimize to Tray")
        minimize_action.triggered.connect(self._minimize_to_tray)
        menu.addSeparator()
        quit_action = menu.addAction("Exit")
        quit_action.triggered.connect(self._quit_application)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.activated.connect(self._on_tray_activated)
        self.tray_icon.show()

        # Expose a "Minimize to Tray" action reachable from the window too.
        self._minimize_action = minimize_action

    def _on_tray_activated(self, reason) -> None:
        if reason == QSystemTrayIcon.DoubleClick:
            self._restore_from_tray()

    def _restore_from_tray(self) -> None:
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def _minimize_to_tray(self) -> None:
        self.hide()
        self.tray_icon.showMessage(
            APP_NAME, "Still running in the background.", QSystemTrayIcon.Information, 2000
        )

    # ---- Shortcuts ----

    def _build_shortcuts(self) -> None:
        new_task_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        new_task_shortcut.activated.connect(self._focus_new_task)

        refresh_shortcut = QShortcut(QKeySequence("F5"), self)
        refresh_shortcut.activated.connect(self._refresh_current_page)

        minimize_shortcut = QShortcut(QKeySequence("Ctrl+M"), self)
        minimize_shortcut.activated.connect(self._minimize_to_tray)

        delete_shortcut = QShortcut(QKeySequence(Qt.Key_Delete), self)
        delete_shortcut.activated.connect(self._delete_selected_task)

    def _delete_selected_task(self) -> None:
        if self.pages.currentWidget() is self.dashboard_page:
            self.dashboard_page.delete_selected_task()

    def _focus_new_task(self) -> None:
        self.pages.setCurrentWidget(self.dashboard_page)
        self.dashboard_page.task_input.setFocus()

    def _refresh_current_page(self) -> None:
        current = self.pages.currentWidget()
        if current is self.dashboard_page:
            self.dashboard_page.refresh_tasks()
            self.dashboard_page.refresh_meetings()
        elif current is self.history_page:
            self.history_page.refresh()

    # ---- Meeting notifications ----

    def _on_meeting_notified(self, title: str) -> None:
        self.dashboard_page.refresh_meetings()

    # ---- Geometry persistence ----

    def _restore_geometry(self) -> None:
        geometry = self._app_settings.load_geometry()
        if geometry is not None:
            self.restoreGeometry(geometry)
        else:
            self.resize(1080, 720)

    def _save_geometry(self) -> None:
        self._app_settings.save_geometry(self.saveGeometry())

    # ---- Shutdown / close behavior ----

    def _quit_application(self) -> None:
        self._is_quitting = True
        self.close()

    def closeEvent(self, event) -> None:
        """Closing the window (X button) always archives pending tasks
        and fully exits the application, per product requirements."""
        try:
            archived_count = self._task_service.archive_all_pending_on_close()
            logger.info("Archived %d pending task(s) on close.", archived_count)
        except Exception as exc:
            logger.error("Failed to archive pending tasks on close: %s", exc)
            QMessageBox.warning(
                self,
                "Warning",
                f"Could not archive pending tasks before closing:\n{exc}",
            )

        self._save_geometry()
        self._meeting_monitor.stop()
        self.tray_icon.hide()
        event.accept()
