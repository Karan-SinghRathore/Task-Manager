"""
Small reusable animation helpers (fade-in for newly inserted widgets/pages).
"""
from PySide6.QtCore import QEasingCurve, QPropertyAnimation
from PySide6.QtWidgets import QGraphicsOpacityEffect


def fade_in(widget, duration: int = 220):
    """Fades a widget from transparent to opaque. Keeps a reference to the
    effect/animation on the widget itself so they aren't garbage collected
    mid-animation.
    """
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b"opacity", widget)
    animation.setDuration(duration)
    animation.setStartValue(0.0)
    animation.setEndValue(1.0)
    animation.setEasingCurve(QEasingCurve.OutCubic)

    widget._fade_effect = effect
    widget._fade_animation = animation
    animation.start()
    return animation
