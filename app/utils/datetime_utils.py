"""
Small helpers for formatting and combining dates/times consistently
across the UI and database layers.
"""
from datetime import datetime

from app.config import DATE_DISPLAY_FORMAT, TIME_DISPLAY_FORMAT


def now() -> datetime:
    return datetime.now()


def split_date_time(dt: datetime):
    """Return (date_str, time_str) for display, e.g. ('2026-08-03', '01:20 PM')."""
    return dt.strftime(DATE_DISPLAY_FORMAT), dt.strftime(TIME_DISPLAY_FORMAT)


def combine_date_time(qdate, qtime) -> datetime:
    """Combine a QDate and QTime into a python datetime."""
    return datetime(
        qdate.year(),
        qdate.month(),
        qdate.day(),
        qtime.hour(),
        qtime.minute(),
        qtime.second(),
    )


def format_meeting_when(meeting_dt: datetime) -> str:
    """e.g. '1:20 PM' for the meeting card header (no leading zero on hour)."""
    if not hasattr(meeting_dt, "strftime"):
        return ""
    text = meeting_dt.strftime(TIME_DISPLAY_FORMAT)  # '01:20 PM'
    if text.startswith("0"):
        text = text[1:]
    return text
