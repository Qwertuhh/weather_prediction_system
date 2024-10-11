# style_sheet.py

light_stylesheet = """
QWidget {
    font-family: Arial, sans-serif;  /* Change to your desired font */
}

QComboBox {
    border: 2px solid #5D5D5D;  /* Dark Gray Border */
    border-radius: 10px;        /* Rounded Corners */
    padding: 5px;               /* Padding inside the ComboBox */
    background-color: #F0F0F0;  /* Light Gray Background */
    min-width: 150px;           /* Minimum width for consistency */
}

QComboBox::drop-down {
    border: 0;                  /* No border for dropdown */
    width: 0px;                 /* Hide the dropdown arrow */
}

QComboBox::item {
    background-color: #F0F0F0;  /* Background for items */
    color: #333;                /* Dark text color */
}

QComboBox::item:selected {
    background-color: #A0C4FF;  /* Light Blue on selection */
}

QMainWindow {
    background-color: #FFFFFF;  /* Main window background */
}

QWebEngineView {
    border: 2px solid #5D5D5D;  /* Border around the map */
    border-radius: 10px;        /* Rounded Corners for map */
}

QPushButton {
    border-radius: 10px;        /* Rounded Corners for buttons */
    background-color: #E0E0E0;  /* Light Button Background */
    color: #333;                /* Dark Text for Button */
    padding: 8px;               /* Padding inside Button */
}

QPushButton:hover {
    background-color: #C0C0C0;  /* Lighter Gray on hover */
}
"""

dark_stylesheet = """
QWidget {
    font-family: Arial, sans-serif;  /* Change to your desired font */
}

QComboBox {
    background-color: #4A4A4A;  /* Dark Gray Background for ComboBox */
    color: #FFFFFF;              /* White Text for ComboBox */
    border: 2px solid #6A6A6A;  /* Lighter Border */
    border-radius: 10px;        /* Rounded Corners */
    padding: 5px;               /* Padding inside the ComboBox */
    min-width: 150px;           /* Minimum width for consistency */
}

QComboBox::drop-down {
    border: 0;                  /* No border for dropdown */
    width: 0px;                 /* Hide the dropdown arrow */
}

QPushButton {
    border-radius: 10px;        /* Rounded Corners for buttons */
    background-color: #4A4A4A;  /* Dark Gray Background for Button */
    color: #FFFFFF;              /* White Text for Button */
    padding: 8px;               /* Padding inside Button */
}

QPushButton:hover {
    background-color: #5A5A5A;  /* Lighter Dark Gray on hover */
}

QWidget#darkMode {
    background-color: #2E2E2E;  /* Dark Background */
    color: #FFFFFF;              /* White Text */
}

QWebEngineView {
    border: 2px solid #6A6A6A;  /* Border around the map */
    border-radius: 10px;        /* Rounded Corners for map */
}

QMainWindow {
    background-color: #2E2E2E;  /* Dark Main window background */
}
"""
