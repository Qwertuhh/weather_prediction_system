import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QComboBox, QTabWidget,
                           QStyleFactory, QMenu, QAction, QLabel, QFrame,
                           QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from datetime import datetime
import glob
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CustomFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #2B2B2B;
                border-radius: 10px;
                padding: 10px;
            }
        """)

class StyledButton(QPushButton):
    def __init__(self, text, color="#4A90E2"):
        super().__init__(text)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 5px;
                padding: 8px 15px;
                color: white;
                font-weight: bold;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {self.adjust_color(color, 20)};
            }}
            QPushButton:pressed {{
                background-color: {self.adjust_color(color, -20)};
            }}
        """)
        
    def adjust_color(self, color, amount):
        # Adjust color brightness
        r = int(color[1:3], 16) + amount
        g = int(color[3:5], 16) + amount
        b = int(color[5:7], 16) + amount
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        return f"#{r:02x}{g:02x}{b:02x}"

class StyledComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QComboBox {
                background-color: #333333;
                border-radius: 5px;
                padding: 8px;
                color: white;
                border: 1px solid #555555;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #333333;
                selection-background-color: #4A90E2;
                selection-color: white;
                border: 1px solid #555555;
            }
        """)

class PlotWidget(QWidget):
    def __init__(self, file_path, dark_mode=True):
        super().__init__()
        self.file_path = file_path
        self.dark_mode = dark_mode
        self.setup_ui()
        
    def setup_ui(self):
        try:
            layout = QVBoxLayout()
            self.figure = Figure(facecolor='#2B2B2B' if self.dark_mode else 'white')
            self.canvas = FigureCanvas(self.figure)
            layout.addWidget(self.canvas)
            self.setLayout(layout)
            self.plot_data()
        except Exception as e:
            logger.error(f"Error in PlotWidget setup_ui: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to setup plot: {str(e)}")
        
    def plot_data(self):
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            logger.debug(f"Loading data from: {self.file_path}")
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"File not found: {self.file_path}")
                
            df = pd.read_csv(self.file_path)
            df['Time'] = pd.to_datetime(df['Time'])
            
            # Plot with custom styles
            ax.plot(df['Time'], df['Temp'], label='Temperature', color='#FF6B6B', linewidth=2)
            ax.plot(df['Time'], df['Humi'], label='Humidity', color='#4ECDC4', linewidth=2)
            ax.plot(df['Time'], df['AIQ'], label='AQI', color='#45B7D1', linewidth=2)
            
            ax.set_xlabel('Time', fontsize=10, color='white' if self.dark_mode else 'black')
            ax.set_ylabel('Values', fontsize=10, color='white' if self.dark_mode else 'black')
            ax.legend(facecolor='#2B2B2B' if self.dark_mode else 'white', 
                     edgecolor='#555555',
                     fontsize=9)
            ax.grid(True, linestyle='--', alpha=0.3)
            
            # Style customization
            if self.dark_mode:
                self.figure.patch.set_facecolor('#2B2B2B')
                ax.set_facecolor('#2B2B2B')
                ax.tick_params(colors='white')
                legend = ax.get_legend()
                plt.setp(legend.get_texts(), color='white')
                
            for spine in ax.spines.values():
                spine.set_color('#555555')
                
            self.figure.autofmt_xdate()
            self.canvas.draw()
            
        except Exception as e:
            logger.error(f"Error in plot_data: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to plot data: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Line Graph Data Visualization")
        self.setGeometry(100, 100, 1200, 800)
        self.dark_mode = True
        self.setup_ui()
        self.check_directory_structure()
        self.setWindowIcon(QIcon('plots/logo.ico'))
        
    def check_directory_structure(self):
        try:
            required_dirs = [
                'data/raw/HADC',
                'data/raw/LADC'
            ]
            
            for dir_path in required_dirs:
                if not os.path.exists(dir_path):
                    logger.warning(f"Directory not found: {dir_path}")
                    QMessageBox.warning(self, "Warning", 
                                      f"Required directory not found: {dir_path}\n"
                                      "Please check your directory structure.")
                else:
                    logger.info(f"Directory found: {dir_path}")
                    
            self.update_file_list()
        except Exception as e:
            logger.error(f"Error checking directory structure: {str(e)}")
            QMessageBox.critical(self, "Error", 
                               "Failed to check directory structure. "
                               "Please verify your setup.")
        
    def setup_ui(self):
        try:
            # Main widget and layout
            main_widget = QWidget()
            self.setCentralWidget(main_widget)
            main_layout = QVBoxLayout()
            
            # Title and header
            header = QHBoxLayout()
            title = QLabel("Line Graph Data Visualization")
            title.setStyleSheet("""
                QLabel {
                    color: #4A90E2;
                    font-size: 24px;
                    font-weight: bold;
                    padding: 10px;
                }
            """)
            header.addWidget(title)
            header.addStretch()
            
            # Control panel
            control_panel = CustomFrame()
            control_layout = QHBoxLayout(control_panel)
            
            # File selection
            self.file_combo = StyledComboBox()
            self.file_combo.setMinimumWidth(300)
            
            # Buttons
            self.theme_button = StyledButton("Toggle Theme", "#FF6B6B")
            self.realtime_button = StyledButton("Start Real-time", "#4ECDC4")
            
            control_layout.addWidget(QLabel("Select File:"))
            control_layout.addWidget(self.file_combo)
            control_layout.addWidget(self.theme_button)
            control_layout.addWidget(self.realtime_button)
            control_layout.addStretch()
            
            # Tab widget styling
            self.tab_widget = QTabWidget()
            self.tab_widget.setStyleSheet("""
                QTabWidget::pane {
                    border: 1px solid #555555;
                    border-radius: 5px;
                    background: #2B2B2B;
                }
                QTabBar::tab {
                    background: #333333;
                    color: white;
                    padding: 8px 20px;
                    border-top-left-radius: 5px;
                    border-top-right-radius: 5px;
                    margin-right: 2px;
                }
                QTabBar::tab:selected {
                    background: #4A90E2;
                }
                QTabBar::tab:hover {
                    background: #555555;
                }
            """)
            self.tab_widget.setTabsClosable(True)
            
            # Layout assembly
            main_layout.addLayout(header)
            main_layout.addWidget(control_panel)
            main_layout.addWidget(self.tab_widget)
            main_widget.setLayout(main_layout)
            
            # Connect signals
            self.theme_button.clicked.connect(self.toggle_theme)
            self.realtime_button.clicked.connect(self.toggle_realtime)
            self.file_combo.currentTextChanged.connect(self.plot_selected_file)
            self.tab_widget.tabCloseRequested.connect(self.close_tab)
            self.file_combo.setContextMenuPolicy(Qt.CustomContextMenu)
            self.file_combo.customContextMenuRequested.connect(self.show_context_menu)
            
            # Set initial theme
            self.apply_theme()
            
        except Exception as e:
            logger.error(f"Error in setup_ui: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to setup UI: {str(e)}")
            
    def update_file_list(self):
        try:
            self.file_combo.clear()
            
            # Get all CSV files
            hadc_path = 'data/raw/HADC'
            ladc_path = 'data/raw/LADC'
            
            hadc_files = glob.glob(f'{hadc_path}/*.csv') if os.path.exists(hadc_path) else []
            ladc_files = glob.glob(f'{ladc_path}/*.csv') if os.path.exists(ladc_path) else []
            
            # Filter out location.csv files
            all_files = [f for f in (hadc_files + ladc_files) if 'location.csv' not in f]
            
            if not all_files:
                logger.warning("No data files found")
                QMessageBox.warning(self, "Warning", "No data files found in the specified directories.")
            
            for file in all_files:
                self.file_combo.addItem(file)
                
        except Exception as e:
            logger.error(f"Error updating file list: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to update file list: {str(e)}")
            
    def apply_theme(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1E1E1E;
                }
                QWidget {
                    background-color: #1E1E1E;
                    color: white;
                }
                QLabel {
                    color: white;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: white;
                }
                QWidget {
                    background-color: white;
                    color: black;
                }
                QLabel {
                    color: black;
                }
            """)

    # [Rest of the methods remain the same as in the previous version]
    def plot_selected_file(self):
        file_path = self.file_combo.currentText()
        if file_path:
            self.add_plot_tab(file_path)
            
    def add_plot_tab(self, file_path, new_tab=False):
        try:
            plot_widget = PlotWidget(file_path, self.dark_mode)
            tab_name = os.path.basename(file_path)
            
            if new_tab or self.tab_widget.count() == 0:
                self.tab_widget.addTab(plot_widget, tab_name)
                self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)
            else:
                self.tab_widget.removeTab(self.tab_widget.currentIndex())
                self.tab_widget.addTab(plot_widget, tab_name)
        except Exception as e:
            logger.error(f"Error adding plot tab: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to add plot tab: {str(e)}")
            
    def close_tab(self, index):
        self.tab_widget.removeTab(index)
        
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        self.theme_button.setText("Dark Mode" if self.dark_mode else "Light Mode")
        
        # Update all plot widgets
        for i in range(self.tab_widget.count()):
            plot_widget = self.tab_widget.widget(i)
            plot_widget.dark_mode = self.dark_mode
            plot_widget.plot_data()
            
    def show_context_menu(self, position):
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #333333;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item {
                padding: 5px 20px;
                border-radius: 3px;
            }
            QMenu::item:selected {
                background-color: #4A90E2;
            }
        """)
        new_window_action = QAction("Plot in New Tab", self)
        new_window_action.triggered.connect(
            lambda: self.add_plot_tab(self.file_combo.currentText(), True))
        menu.addAction(new_window_action)
        menu.exec_(self.file_combo.mapToGlobal(position))
        
    def toggle_realtime(self):
        self.realtime_active = not getattr(self, 'realtime_active', False)
        if self.realtime_active:
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_plot)
            self.timer.start(900)  # Update every 0.9 seconds
            self.realtime_button.setText("Stop Real-time")
            self.realtime_button.setStyleSheet("""
                QPushButton {
                    background-color: #FF6B6B;
                    border-radius: 5px;
                    padding: 8px 15px;
                    color: white;
                    font-weight: bold;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #FF8888;
                }
            """)
        else:
            if hasattr(self, 'timer'):
                self.timer.stop()
            self.realtime_button.setText("Start Real-time")
            self.realtime_button.setStyleSheet("""
                QPushButton {
                    background-color: #4ECDC4;
                    border-radius: 5px;
                    padding: 8px 15px;
                    color: white;
                    font-weight: bold;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #65E5DC;
                }
            """)
            
    def update_plot(self):
        try:
            current_file = self.file_combo.currentText()
            if current_file and self.tab_widget.count() > 0:
                current_tab = self.tab_widget.currentWidget()
                current_tab.plot_data()
                logger.debug(f"Real-time update completed for file: {current_file}")
        except Exception as e:
            logger.error(f"Error in real-time update: {str(e)}")
            self.toggle_realtime()  # Stop real-time updates on error
            QMessageBox.warning(self, "Warning", 
                              "Real-time updates stopped due to an error.")

def main():
    try:
        app = QApplication(sys.argv)
        
        # Set application-wide style
        app.setStyle(QStyleFactory.create("Fusion"))
        
        # Set default font
        font = QFont("Segoe UI", 10)
        app.setFont(font)
        
        # Enable High DPI scaling
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec_())
    except Exception as e:
        logger.critical(f"Application failed to start: {str(e)}")
        QMessageBox.critical(None, "Critical Error", 
                           f"Application failed to start: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user.")