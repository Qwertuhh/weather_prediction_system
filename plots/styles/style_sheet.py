# style_sheet.py

light_stylesheet = """
QWidget {
    font-family: Arial, sans-serif;
}

QMainWindow {
    background-color: #F5F5F5;
}

QToolBar {
    background-color: #E0E0E0;
    border: none;
    spacing: 10px;
    padding: 5px;
}

QToolButton {
    color: #333333;
    background-color: transparent;
    border: none;
    padding: 5px;
    font-weight: bold;
    font-size: 12px;
}

QToolButton:hover {
    background-color: #C0C0C0;
    border-radius: 5px;
}

QToolButton:pressed {
    background-color: #A0A0A0;
    border-radius: 5px;
}

QComboBox {
    border: 2px solid #5D5D5D;
    border-radius: 5px;
    padding: 5px;
    background-color: #FFFFFF;
    min-width: 150px;
    color: #333333;
}

QComboBox::drop-down {
    border: 0;
    width: 30px;
}

QComboBox::down-arrow {
    image: url(icons/dropdown_arrow_dark.png);
}

QComboBox::item {
    background-color: #FFFFFF;
    color: #333333;
}

QComboBox::item:selected {
    background-color: #E6E6E6;
}

QWebEngineView {
    border: 2px solid #CCCCCC;
    border-radius: 5px;
}
"""

dark_stylesheet = """
QWidget {
    font-family: Arial, sans-serif;
}

QMainWindow {
    background-color: #2E2E2E;
}

QToolBar {
    background-color: #3A3A3A;
    border: none;
    spacing: 10px;
    padding: 5px;
}

QToolButton {
    color: #FFFFFF;
    background-color: transparent;
    border: none;
    padding: 5px;
    font-weight: bold;
    font-size: 12px;
}

QToolButton:hover {
    background-color: #4A4A4A;
    border-radius: 5px;
}

QToolButton:pressed {
    background-color: #5A5A5A;
    border-radius: 5px;
}

QComboBox {
    background-color: #4A4A4A;
    color: #FFFFFF;
    border: 2px solid #6A6A6A;
    border-radius: 5px;
    padding: 5px;
    min-width: 150px;
}

QComboBox::drop-down {
    border: 0;
    width: 30px;
}

QComboBox::down-arrow {
    image: url(icons/dropdown_arrow_light.png);
}

QComboBox::item {
    background-color: #4A4A4A;
    color: #FFFFFF;
}

QComboBox::item:selected {
    background-color: #5A5A5A;
}

QWebEngineView {
    border: 2px solid #6A6A6A;
    border-radius: 5px;
}
"""