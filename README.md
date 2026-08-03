<div align="center">

# 📋 Task Manager

**A native Windows desktop task manager with meeting reminders.**

Python 3 · PySide6 · MongoDB · PyInstaller

![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-0078D6)
![Python](https://img.shields.io/badge/python-3.10%2B-3776AB)
![UI](https://img.shields.io/badge/UI-PySide6%20(Qt)-41CD52)
![Database](https://img.shields.io/badge/database-MongoDB-47A248)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

</div>

---

No browser. No web server. No login. No internet requirement.
Double-click the executable and it opens immediately.

This is a **real native desktop app** — not Electron, not a website in a
window. It's built directly on Qt (PySide6), so it looks, feels, and
performs like a proper Windows program.

## ✨ Features

- **Dashboard** — add tasks by pressing `Enter` or clicking `+`, check
  them off to complete, or delete them permanently.
- **History** — every completed or closed-pending task is archived here
  with its status, date, and time. Search, delete individual entries, or
  clear all history in one click.
- **Meeting reminders** — schedule a meeting with a title, date, time,
  and reminder window (default 10 minutes). A native Windows toast
  notification fires exactly once, the configured number of minutes
  before the meeting starts.
- **Auto-archive on close** — any tasks still pending when you close the
  app are automatically moved into History with status `Pending` and the
  closing date/time. The Dashboard is always empty on next launch.
- **System tray** — minimize to tray from the tray menu; double-click
  the tray icon to restore. Closing the window (`X`) always exits the
  app and runs the archive step first.
- **Keyboard shortcuts** — `Ctrl+N` new task · `F5` refresh · `Delete`
  removes the selected task · `Ctrl+M` minimize to tray.
- **Remembers window size & position** between launches.
- **Modern dark UI** — rounded corners, smooth fade-in animations, and a
  Windows 11–inspired color palette.

## 🛠 Tech stack

| Concern              | Library                     |
|-----------------------|------------------------------|
| UI                    | PySide6 (Qt for Python)     |
| Database              | MongoDB (local) via PyMongo |
| Toast notifications   | `windows-toasts`            |
| Packaging             | PyInstaller                 |

Explicitly **not used**: Flask, Django, React, Electron, HTML/CSS, SQLite.

## 📁 Project structure

```
main.py                    Entry point — connects to Mongo, launches the UI

app/
├─ config.py               Constants (Mongo URI, DB/collection names, defaults)
├─ core/                    Business logic — independent of Qt and Mongo details
│  ├─ task_service.py        add / complete / delete tasks, archive-on-close
│  ├─ history_service.py     list / search / delete / clear history
│  └─ meeting_service.py     add meetings, find meetings due for a reminder
├─ db/                       MongoDB access layer
│  ├─ connection.py           connection lifecycle + friendly failure handling
│  ├─ tasks_repo.py
│  ├─ history_repo.py
│  ├─ meetings_repo.py
│  └─ repositories.py         wires repositories to the shared connection
├─ notifications/
│  ├─ toast.py                Windows toast wrapper (never raises)
│  └─ meeting_monitor.py      QTimer that polls Mongo for due meetings
├─ ui/
│  ├─ theme.py                dark Windows 11–style QSS stylesheet
│  ├─ main_window.py          window shell, tray icon, shortcuts, close handling
│  ├─ sidebar.py              left navigation (Dashboard / History)
│  ├─ dashboard_page.py       add-task card, task list, meeting reminder card
│  ├─ history_page.py         search, list, delete, clear history
│  ├─ animations.py           fade-in helper used when inserting cards
│  └─ widgets/                TaskCard, MeetingCard, HistoryRow, EmptyState
└─ utils/
   ├─ settings.py             QSettings-backed window geometry persistence
   └─ datetime_utils.py       date/time formatting helpers

assets/
├─ icon.svg                 Source icon (dark, blue accent, checklist)
└─ icon.ico                 Generated multi-resolution icon (16–256 px)

scripts/
└─ generate_icon.py         Regenerates icon.ico from icon.svg via Qt's SVG renderer

TaskManager.spec            PyInstaller build spec
requirements.txt
```

## ✅ Prerequisites

- Windows 10 / 11
- Python 3.10+ on `PATH`
- [MongoDB Community Server](https://www.mongodb.com/try/download/community)
  installed and running locally as a service (default:
  `mongodb://localhost:27017`)

## 🚀 Getting started

```powershell
git clone <this-repo-url>
cd task-manager
pip install -r requirements.txt
python main.py
```

If MongoDB isn't running, the app shows a friendly dialog —
*"MongoDB is not running. Please start the MongoDB service."* — instead
of crashing.

## 🎨 Regenerating the icon

The app icon is authored as `assets/icon.svg` and converted to a
multi-resolution `.ico` (16, 32, 48, 64, 128, 256 px) using Qt's own SVG
renderer — no native Cairo/GTK dependency required. Re-run this whenever
you edit the SVG:

```powershell
python scripts/generate_icon.py
```

## 📦 Building the standalone .exe

```powershell
pyinstaller TaskManager.spec
```

This produces a `dist/TaskManager/` folder containing `TaskManager.exe`
plus its supporting files — a "onedir" build, recommended for PySide6
apps since it starts faster and avoids some antivirus false positives
compared to a single-file build. The executable:

- Uses `assets/icon.ico` as both the window icon and the .exe icon.
- Runs windowed (no console popup).
- Bundles `assets/icon.ico` / `icon.svg` alongside itself so toast
  notifications and the window icon work correctly when frozen.

Launch it with:

```powershell
dist\TaskManager\TaskManager.exe
```

Copy the entire `dist\TaskManager\` folder wherever you like — it's
self-contained and does **not** require Python on the target machine.
(MongoDB is still required locally.)

## 🗄 Database

| | |
|---|---|
| **Database** | `task_manager` |
| **Collections** | `tasks` — pending dashboard items · `history` — archived completed/pending tasks · `meetings` — scheduled reminders |

No SQLite, no cloud database — everything stays local on your machine.

## 📝 Behavior notes

- Closing the main window (`X`) always archives any pending tasks to
  History with status `Pending` and the current date/time, then exits
  the application.
- Use the tray icon's **Minimize to Tray** action (or `Ctrl+M`) to keep
  the app running in the background — the meeting monitor keeps polling
  for due reminders while minimized.
- Each meeting notification fires exactly once: the meeting document is
  marked `notified: true` in MongoDB immediately after the toast is
  shown.

## 📄 License

MIT — see [LICENSE](LICENSE).
