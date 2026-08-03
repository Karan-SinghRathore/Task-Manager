"""
Persists lightweight app preferences (window geometry/position, tray behavior)
using QSettings, which stores to the Windows registry under HKCU.
"""
from PySide6.QtCore import QSettings

from app.config import APP_NAME, APP_ORG


class AppSettings:
    """Thin wrapper around QSettings for window geometry persistence."""

    def __init__(self):
        self._settings = QSettings(APP_ORG, APP_NAME)

    def save_geometry(self, geometry: bytes):
        self._settings.setValue("window/geometry", geometry)

    def load_geometry(self):
        return self._settings.value("window/geometry")

    def save_window_state(self, state: bytes):
        self._settings.setValue("window/state", state)

    def load_window_state(self):
        return self._settings.value("window/state")
