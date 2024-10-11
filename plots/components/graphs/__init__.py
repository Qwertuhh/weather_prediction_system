import os
import sys
import pandas as pd
import folium
from PyQt5.QtWebEngineWidgets import QWebEngineView  # Correct import for QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from folium.plugins import HeatMap
from styles.style_sheet import light_stylesheet, dark_stylesheet
from heatmap import load_map
from windmap import WindDataVisualizer

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

        self.folium_map_path = "plots/components/html/folium.html"
        self.load_geojson_files()

        self.geojson_dropdown.currentIndexChanged.connect(self.update_map_with_geojson)

        self.map_view = QWebEngineView(self)
        self.layout.addWidget(self.map_view)

        self.toggle_button = QPushButton("Toggle Dark Mode", self)
        self.toggle_button.clicked.connect(self.toggle_mode)
        self.layout.addWidget(self.toggle_button)

        # Initialize WindDataVisualizer
        self.ladc_file = 'data/raw/LADC/__locations__.csv'
        self.hadc_file = 'data/raw/HADC/Location_1.csv'
        self.wind_visualizer = WindDataVisualizer(self.ladc_file, self.hadc_file)
        self.geojson_dir = 'data/maps/jaipur'

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
        added_files = set()
        for file_name in os.listdir('data/maps/jaipur'):
            if file_name.endswith('.geojson'):
                base_name = file_name[:-8]
                if base_name not in added_files:
                    self.geojson_dropdown.addItem(base_name)
                    added_files.add(base_name)

    def load_map(self, geojson_file=None):
        """Load the Folium map and display it in the QWebEngineView."""
        folium_map = load_map(self.folium_map_path, geojson_file)

        # Load HADC data for heatmap visualization
        self.load_hadc_heatmap(folium_map)

        # Save the updated map
        folium_map.save(self.folium_map_path)
        self.map_view.setUrl(QUrl.fromLocalFile(os.path.abspath(self.folium_map_path)))

        # Call load_map() with the desired GeoJSON file name
        load_map(self.folium_map_path, geojson_file="jaipur_Zones")

        # Add wind arrows and markers to the Folium map after it is loaded
        #? Using compound method to plot
        self.wind_visualizer.add_wind_arrows_and_markers()

    def load_hadc_heatmap(self, folium_map):
        """Load HADC data and plot it as a heatmap."""
        try:
            hadc_data = self.wind_visualizer.load_hadc_data()
            if hadc_data is not None:
                heatmap_data = [(row['Latitude'], row['Longitude']) for _, row in hadc_data.iterrows() if 'Latitude' in row and 'Longitude' in row]
                HeatMap(heatmap_data).add_to(folium_map)
        except Exception as e:
            print(f"Error loading HADC data for heatmap: {e}")

    def update_map_with_geojson(self):
        """Update the map when the selected GeoJSON file changes."""
        selected_geojson = self.geojson_dropdown.currentText()
        self.load_map(selected_geojson)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherMapApp()
    window.show()
    sys.exit(app.exec_())
