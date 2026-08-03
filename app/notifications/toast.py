"""
Windows Toast Notification wrapper around the `windows-toasts` package.
Failures here must never crash the app - a missing/broken notification
backend should just be logged and skipped.
"""
import logging

from app.config import APP_NAME, ICON_PATH

logger = logging.getLogger(__name__)


class ToastNotifier:
    def __init__(self):
        self._notifier = None
        try:
            from windows_toasts import Toast, ToastDisplayImage, WindowsToaster

            self._Toast = Toast
            self._ToastDisplayImage = ToastDisplayImage
            self._notifier = WindowsToaster(APP_NAME)
        except Exception as exc:  # pragma: no cover - platform dependent
            logger.warning("Toast notifications unavailable: %s", exc)

    def show(self, title: str, message: str) -> None:
        if self._notifier is None:
            return
        try:
            toast = self._Toast([title, message])
            if ICON_PATH.exists():
                toast.AddImage(self._ToastDisplayImage.fromPath(str(ICON_PATH)))
            self._notifier.show_toast(toast)
        except Exception as exc:  # pragma: no cover - platform dependent
            logger.warning("Failed to show toast notification: %s", exc)


toast_notifier = ToastNotifier()
