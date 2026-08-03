"""
Centralized dark, Windows 11-inspired color palette and QSS stylesheet.
Keeping this in one place lets every widget share consistent styling
without duplicating hex codes across the UI files.
"""

# --- Palette ---
COLOR_BG = "#0f1117"
COLOR_SURFACE = "#171a23"
COLOR_SURFACE_ALT = "#1d212c"
COLOR_CARD = "#20242f"
COLOR_CARD_HOVER = "#262b38"
COLOR_BORDER = "#2a2f3d"
COLOR_TEXT_PRIMARY = "#e8eaf0"
COLOR_TEXT_SECONDARY = "#9aa2b2"
COLOR_TEXT_MUTED = "#6b7280"
COLOR_ACCENT = "#4da3ff"
COLOR_ACCENT_HOVER = "#69b4ff"
COLOR_ACCENT_PRESSED = "#3a86e0"
COLOR_DANGER = "#ef5a6f"
COLOR_DANGER_HOVER = "#f4788a"
COLOR_SUCCESS = "#3ecf8e"

FONT_FAMILY = "Segoe UI Variable, Segoe UI, Inter, Arial"

STYLESHEET = f"""
QWidget {{
    background-color: {COLOR_BG};
    color: {COLOR_TEXT_PRIMARY};
    font-family: "{FONT_FAMILY}";
    font-size: 14px;
}}

#Sidebar {{
    background-color: {COLOR_SURFACE};
    border-right: 1px solid {COLOR_BORDER};
}}

#SidebarTitle {{
    color: {COLOR_TEXT_PRIMARY};
    font-size: 17px;
    font-weight: 600;
    padding: 22px 20px 18px 20px;
}}

QPushButton#NavButton {{
    background-color: transparent;
    color: {COLOR_TEXT_SECONDARY};
    border: none;
    border-radius: 10px;
    text-align: left;
    padding: 12px 16px;
    font-size: 14px;
    font-weight: 500;
}}

QPushButton#NavButton:hover {{
    background-color: {COLOR_SURFACE_ALT};
    color: {COLOR_TEXT_PRIMARY};
}}

QPushButton#NavButton:checked {{
    background-color: {COLOR_CARD};
    color: {COLOR_ACCENT};
    font-weight: 600;
}}

#PageContainer {{
    background-color: {COLOR_BG};
}}

#PageTitle {{
    font-size: 22px;
    font-weight: 600;
    color: {COLOR_TEXT_PRIMARY};
}}

#SectionCard {{
    background-color: {COLOR_SURFACE};
    border: 1px solid {COLOR_BORDER};
    border-radius: 16px;
}}

#TaskCard, #MeetingCard, #HistoryRow {{
    background-color: {COLOR_CARD};
    border: 1px solid {COLOR_BORDER};
    border-radius: 12px;
}}

#TaskCard:hover, #MeetingCard:hover, #HistoryRow:hover {{
    background-color: {COLOR_CARD_HOVER};
}}

QLineEdit, QDateEdit, QTimeEdit, QSpinBox {{
    background-color: {COLOR_SURFACE_ALT};
    border: 1px solid {COLOR_BORDER};
    border-radius: 10px;
    padding: 10px 14px;
    color: {COLOR_TEXT_PRIMARY};
    font-size: 14px;
    selection-background-color: {COLOR_ACCENT};
}}

QLineEdit:focus, QDateEdit:focus, QTimeEdit:focus, QSpinBox:focus {{
    border: 1px solid {COLOR_ACCENT};
}}

QLineEdit::placeholder {{
    color: {COLOR_TEXT_MUTED};
}}

QPushButton#PrimaryButton {{
    background-color: {COLOR_ACCENT};
    color: #0b0d12;
    border: none;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 600;
    font-size: 14px;
}}

QPushButton#PrimaryButton:hover {{
    background-color: {COLOR_ACCENT_HOVER};
}}

QPushButton#PrimaryButton:pressed {{
    background-color: {COLOR_ACCENT_PRESSED};
}}

QPushButton#AddButton {{
    background-color: {COLOR_ACCENT};
    color: #0b0d12;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    font-size: 18px;
}}

QPushButton#AddButton:hover {{
    background-color: {COLOR_ACCENT_HOVER};
}}

QPushButton#DangerButton {{
    background-color: transparent;
    color: {COLOR_DANGER};
    border: 1px solid {COLOR_BORDER};
    border-radius: 8px;
    padding: 8px 14px;
    font-weight: 600;
}}

QPushButton#DangerButton:hover {{
    background-color: rgba(239, 90, 111, 0.12);
    border-color: {COLOR_DANGER};
}}

QPushButton#IconDeleteButton {{
    background-color: transparent;
    border: none;
    border-radius: 8px;
    color: {COLOR_TEXT_MUTED};
    font-size: 16px;
    font-weight: 700;
}}

QPushButton#IconDeleteButton:hover {{
    background-color: rgba(239, 90, 111, 0.15);
    color: {COLOR_DANGER};
}}

QCheckBox {{
    spacing: 12px;
}}

QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border-radius: 6px;
    border: 2px solid {COLOR_TEXT_MUTED};
    background-color: transparent;
}}

QCheckBox::indicator:hover {{
    border-color: {COLOR_ACCENT};
}}

QCheckBox::indicator:checked {{
    background-color: {COLOR_SUCCESS};
    border-color: {COLOR_SUCCESS};
}}

QLabel#TaskName {{
    font-size: 15px;
    font-weight: 500;
    color: {COLOR_TEXT_PRIMARY};
}}

QLabel#TaskNameCompleted {{
    font-size: 15px;
    font-weight: 500;
    color: {COLOR_TEXT_MUTED};
    text-decoration: line-through;
}}

QLabel#MutedLabel {{
    color: {COLOR_TEXT_SECONDARY};
    font-size: 12px;
}}

QLabel#EmptyStateTitle {{
    color: {COLOR_TEXT_SECONDARY};
    font-size: 16px;
    font-weight: 600;
}}

QLabel#EmptyStateSubtitle {{
    color: {COLOR_TEXT_MUTED};
    font-size: 13px;
}}

QLabel#StatusPillCompleted {{
    background-color: rgba(62, 207, 142, 0.15);
    color: {COLOR_SUCCESS};
    border-radius: 8px;
    padding: 4px 10px;
    font-size: 12px;
    font-weight: 600;
}}

QLabel#StatusPillPending {{
    background-color: rgba(239, 90, 111, 0.15);
    color: {COLOR_DANGER};
    border-radius: 8px;
    padding: 4px 10px;
    font-size: 12px;
    font-weight: 600;
}}

QScrollArea {{
    border: none;
    background-color: transparent;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 4px;
}}

QScrollBar::handle:vertical {{
    background: {COLOR_BORDER};
    border-radius: 5px;
    min-height: 24px;
}}

QScrollBar::handle:vertical:hover {{
    background: {COLOR_TEXT_MUTED};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QToolTip {{
    background-color: {COLOR_SURFACE_ALT};
    color: {COLOR_TEXT_PRIMARY};
    border: 1px solid {COLOR_BORDER};
    padding: 6px 10px;
    border-radius: 6px;
}}

QMessageBox {{
    background-color: {COLOR_SURFACE};
}}

QSpinBox::up-button, QSpinBox::down-button {{
    width: 18px;
    border: none;
}}
"""
