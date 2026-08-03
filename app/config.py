"""
Application-wide constants and configuration values.
"""
from pathlib import Path

APP_NAME = "Task Manager"
APP_ORG = "TaskManagerApp"

# --- MongoDB ---
MONGO_URI = "mongodb://localhost:27017"
MONGO_SERVER_TIMEOUT_MS = 2500
DB_NAME = "task_manager"
COLLECTION_TASKS = "tasks"
COLLECTION_HISTORY = "history"
COLLECTION_MEETINGS = "meetings"

# --- Meeting monitor ---
MEETING_POLL_INTERVAL_MS = 15_000  # how often to check for due meetings
DEFAULT_REMINDER_MINUTES = 10

# --- Task status values ---
STATUS_COMPLETED = "Completed"
STATUS_PENDING = "Pending"

# --- Paths ---
ROOT_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT_DIR / "assets"
ICON_PATH = ASSETS_DIR / "icon.ico"

# --- Datetime display formats ---
DATE_DISPLAY_FORMAT = "%Y-%m-%d"
TIME_DISPLAY_FORMAT = "%I:%M %p"
