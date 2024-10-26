COLORS = {
    'primary': '#4A90E2',
    'success': '#4ECDC4',
    'warning': '#FFB900',
    'danger': '#FF6B6B',
    'dark': {
        'bg': '#1E1E1E',
        'surface': '#2B2B2B',
        'border': '#555555',
        'text': '#FFFFFF',
        'secondary_text': '#B0B0B0',
        'tab_bg': '#333333',
        'tab_selected': '#4A90E2',
        'tab_hover': '#404040'
    },
    'light': {
        'bg': '#F5F5F5',
        'surface': '#FFFFFF',
        'border': '#E0E0E0',
        'text': '#333333',
        'secondary_text': '#666666',
        'tab_bg': '#EEEEEE',
        'tab_selected': '#4A90E2',
        'tab_hover': '#DDDDDD'
    },
    'hadc': '#4A90E2',
    'ladc': '#45B7D1'
}

def get_theme(dark_mode=True):
    """Get complete theme based on mode"""
    theme = COLORS['dark'] if dark_mode else COLORS['light']
    theme.update({
        'primary': COLORS['primary'],
        'success': COLORS['success'],
        'warning': COLORS['warning'],
        'danger': COLORS['danger'],
        'tab_bg': theme['tab_bg'],
        'selected_bg': theme['tab_selected'],
        'hover_bg': theme['tab_hover']
    })
    return theme

MAIN_WINDOW_STYLE = """
QMainWindow {{
    background-color: {bg};
}}
"""

FRAME_STYLE = """
QFrame {{
    background-color: {surface};
    border-radius: 12px;
    border: 1px solid {border};
}}

QFrame#controlFrame {{
    background-color: {surface};
    border-radius: 8px;
    border: 1px solid {border};
    padding: 12px;
    margin: 8px 0px;
}}
"""

BUTTON_STYLE = """
QPushButton {{
    background-color: {primary};
    border-radius: 6px;
    padding: 8px 16px;
    color: white;
    font-weight: bold;
    border: none;
    min-width: 32px;
    min-height: 32px;
}}

QPushButton:hover {{
    background-color: {hover_bg};
}}

QPushButton:pressed {{
    background-color: {selected_bg};
}}

QPushButton:disabled {{
    background-color: {border};
    color: {secondary_text};
}}
"""

COMBOBOX_STYLE = """
QComboBox {{
    background-color: {surface};
    border-radius: 6px;
    padding: 8px 12px;
    color: {text};
    border: 1px solid {border};
    min-width: 200px;
}}

QComboBox::drop-down {{
    border: none;
    width: 20px;
    padding-right: 8px;
}}

QComboBox::down-arrow {{
    image: url(icons/chevron-down.svg);
    width: 12px;
    height: 12px;
}}

QComboBox QAbstractItemView {{
    background-color: {surface};
    color: {text};
    selection-background-color: {primary};
    selection-color: white;
    border: 1px solid {border};
    border-radius: 6px;
    padding: 4px;
}}
"""

TAB_WIDGET_STYLE = """
QTabWidget::pane {{
    border: 1px solid {border};
    border-radius: 8px;
    background: {surface};
    padding: 2px;
}}

QTabBar::tab {{
    background: {tab_bg};
    color: {text};
    padding: 10px 20px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    background: {selected_bg};
    color: white;
}}

QTabBar::tab:hover:!selected {{
    background: {hover_bg};
}}

QTabBar::close-button {{
    image: url(icons/x.svg);
    padding: 4px;
}}

QTabBar::close-button:hover {{
    background: rgba(255, 255, 255, 0.1);
    border-radius: 2px;
}}
"""

GROUP_BOX_STYLE = """
QGroupBox {{
    background-color: {surface};
    border: 1px solid {border};
    border-radius: 6px;
    margin-top: 12px;
    padding: 12px;
}}

QGroupBox::title {{
    color: {text};
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    background-color: {surface};
}}
"""

LABEL_STYLE = """
QLabel {{
    color: {text};
}}

QLabel#title {{
    color: {primary};
    font-size: 24px;
    font-weight: bold;
    padding: 16px;
}}
"""

STATUS_BAR_STYLE = """
QStatusBar {{
    background-color: {surface};
    color: {text};
    border-top: 1px solid {border};
}}
"""

def apply_theme(widget, dark_mode=True):
    """Apply theme to widget and all its children"""
    theme = get_theme(dark_mode)
    
    widget.setStyleSheet(
        MAIN_WINDOW_STYLE.format(**theme) +
        FRAME_STYLE.format(**theme) +
        BUTTON_STYLE.format(**theme) +
        COMBOBOX_STYLE.format(**theme) +
        TAB_WIDGET_STYLE.format(**theme) +
        GROUP_BOX_STYLE.format(**theme) +
        LABEL_STYLE.format(**theme) +
        STATUS_BAR_STYLE.format(**theme)
    )
