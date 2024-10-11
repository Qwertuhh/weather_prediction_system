import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QToolBar, QAction, QComboBox
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtSvg import QSvgRenderer
import os
from components.map import MapVisualization
from styles.style_sheet import light_stylesheet, dark_stylesheet

class MapApp(QMainWindow):
    def __init__(self):   
        super().__init__()
        self.setWindowTitle("Weather Prediction System")
        self.setGeometry(100, 100, 1200, 800)
        
        self.set_window_icon()
        self.folium_map_path = "plots/components/html/folium.html"

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        self.is_dark_mode = False
        self.create_toolbar()
        self.initUI()
        
        self.setStyleSheet(light_stylesheet)

    def set_window_icon(self):
        renderer = QSvgRenderer('plots/logo.svg')
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        self.setWindowIcon(QIcon(pixmap))

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        self.mode_switch = QAction("Switch Mode", self)
        refresh_action = QAction("Refresh GeoJSON", self)
        toggle_action = QAction("Toggle GeoJSON", self)

        self.mode_switch.triggered.connect(self.switch_mode)
        refresh_action.triggered.connect(self.refresh_geojson)
        toggle_action.triggered.connect(self.toggle_geojson)

        toolbar.addAction(self.mode_switch)
        toolbar.addAction(refresh_action)
        toolbar.addAction(toggle_action)

    def initUI(self):
        self.geojson_dropdown = QComboBox(self)
        self.geojson_dropdown.currentIndexChanged.connect(self.change_geojson_layer)

        self.webview = QWebEngineView(self)

        self.layout.addWidget(self.geojson_dropdown)
        self.layout.addWidget(self.webview)

        self.load_geojson_options()
        initial_geojson = self.geojson_dropdown.currentText()
        self.display_map(initial_geojson)

    def load_geojson_options(self):
        geojson_dir = 'data/maps/Jaipur'
        geojson_files = [f[:-8] for f in os.listdir(geojson_dir) if f.endswith('.geojson')]
        self.geojson_dropdown.clear()
        self.geojson_dropdown.addItems(geojson_files)
        
        if self.geojson_dropdown.count() > 0:
            self.geojson_dropdown.setCurrentIndex(0)

    def change_geojson_layer(self):
        selected_geojson = self.geojson_dropdown.currentText()
        self.display_map(selected_geojson)

    def switch_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        self.setStyleSheet(dark_stylesheet if self.is_dark_mode else light_stylesheet)
        self.refresh_map()
        self.load_geojson_options()
        self.display_map(self.geojson_dropdown.currentText())

    def refresh_geojson(self):
        self.load_geojson_options()
        self.display_map(self.geojson_dropdown.currentText())

    def toggle_geojson(self):
        if self.geojson_dropdown.isVisible():
            self.geojson_dropdown.hide()
        else:
            self.geojson_dropdown.show()

    def display_map(self, selected_geojson):
        ladc_path = 'data/raw/LADC/__locations__.csv'
        hadc_path = 'data/raw/HADC/Location_1.csv'
        MapVisualization.create_wind_map(ladc_path, hadc_path, selected_geojson, self.is_dark_mode)
        self.refresh_map()

    def refresh_map(self):
        self.webview.setUrl(QUrl.fromLocalFile(os.path.abspath(self.folium_map_path)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MapApp()
    window.show()
    sys.exit(app.exec_())