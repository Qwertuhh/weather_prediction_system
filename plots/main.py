import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from styles.style_sheet import light_stylesheet, dark_stylesheet  # Import styles
from plots.components.graphs.heatmap import load_map  # Import load_map function from plotting
from wind_data import WindDataVisualizer  # Import the WindDataVisualizer

class WeatherMapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Weather Map Application')
        self.setGeometry(100, 100, 1200, 800)

        # Initial mode
        self.dark_mode = False
        self.setStyleSheet(light_stylesheet)

        # Set the application icon
        self.setWindowIcon(QIcon('plots/logo.svg'))

        # Create a central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create a dropdown for selecting GeoJSON maps
        self.geojson_dropdown = QComboBox(self)
        self.layout.addWidget(self.geojson_dropdown)

        self.folium_map = "plots/components/html/folium.html"
        self.load_geojson_files()

        self.geojson_dropdown.currentIndexChanged.connect(self.update_map_with_geojson)

        self.map_view = QWebEngineView(self)
        self.layout.addWidget(self.map_view)

        self.toggle_button = QPushButton("Toggle Dark Mode", self)
        self.toggle_button.clicked.connect(self.toggle_mode)
        self.layout.addWidget(self.toggle_button)

        # Load initial map with default GeoJSON
        self.load_map("Jaipur_Zones")

    def toggle_mode(self):
        """Toggle between light mode and dark mode."""
        if self.dark_mode:
            self.setStyleSheet(light_stylesheet)
        else:
            self.setStyleSheet(dark_stylesheet)
        self.dark_mode = not self.dark_mode

    def load_geojson_files(self):
        """Load GeoJSON files from the data/maps/geoJSON directory."""
        geojson_dir = 'data/maps/jaipur'
        added_files = set()
        for file_name in os.listdir(geojson_dir):
            if file_name.endswith('.geojson'):
                base_name = file_name[:-8]
                if base_name not in added_files:
                    self.geojson_dropdown.addItem(base_name)
                    added_files.add(base_name)

    def load_map(self, geojson_file=None):
        """Load the Folium map and display it in the QWebEngineView."""
        folium_map = load_map(self.folium_map, geojson_file)
        self.map_view.setUrl(QUrl.fromLocalFile(os.path.abspath(self.folium_map)))

    def update_map_with_geojson(self):
        """Update the map when the selected GeoJSON file changes."""
        selected_geojson = self.geojson_dropdown.currentText()
        self.load_map(selected_geojson)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherMapApp()
    window.show()
    sys.exit(app.exec_())
