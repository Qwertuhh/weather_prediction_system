import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
import folium
from folium.plugins import HeatMap
import json
from styles.style_sheet import light_stylesheet, dark_stylesheet  # Import styles
import sys

from plots.components.graphs.windmap import WindDataVisualizer  # Import the WindDataVisualizer

#? App Object
class WeatherMapApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Weather Map Application')
        self.setGeometry(100, 100, 1200, 800)

        # Initial mode
        self.dark_mode = False
        self.setStyleSheet(light_stylesheet)  # Set initial style to light mode

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
        
        # Instantiate WindDataVisualizer
        self.wind_data_visualizer = WindDataVisualizer('data/raw/LADC/__locations__.csv', 'data/raw/HADC/location_1.csv')

        # Populate the dropdown with available GeoJSON files
        self.load_geojson_files()

        # Connect dropdown change to map update
        self.geojson_dropdown.currentIndexChanged.connect(self.update_map_with_geojson)

        # Create a map viewer (using QWebEngineView for folium map)
        self.map_view = QWebEngineView(self)
        self.layout.addWidget(self.map_view)

        # Create a toggle button for dark/light mode
        self.toggle_button = QPushButton("Toggle Dark Mode", self)
        self.toggle_button.clicked.connect(self.toggle_mode)
        self.layout.addWidget(self.toggle_button)

        # Load initial map with default GeoJSON
        self.load_map("Jaipur_Zones")  # Load Jaipur_Zones.geojson by default

    def toggle_mode(self):
        """Toggle between light mode and dark mode."""
        if self.dark_mode:
            self.setStyleSheet(light_stylesheet)  # Switch to light mode
            self.central_widget.setObjectName("")  # Reset object name for light mode
        else:
            self.setStyleSheet(dark_stylesheet)  # Switch to dark mode
            self.central_widget.setObjectName("darkMode")  # Set object name for dark mode
        self.central_widget.style().polish(self.central_widget)  # Apply style changes
        self.dark_mode = not self.dark_mode  # Flip the mode

    def load_geojson_files(self):
        """Load GeoJSON files from the data/maps/geoJSON directory."""
        geojson_dir = 'data/maps/jaipur'
        added_files = set()  # Use a set to track added GeoJSON files to prevent duplicates
        for file_name in os.listdir(geojson_dir):
            if file_name.endswith('.geojson'):
                base_name = file_name[:-8]  # Remove .geojson
                if base_name not in added_files:
                    self.geojson_dropdown.addItem(base_name)  # Add item without the .geojson extension
                    added_files.add(base_name)  # Mark as added

    def load_map(self, geojson_file=None):
        """Generate and display the map with optional GeoJSON overlay and tooltips/popups."""
        # Create a base Folium map
        m = folium.Map(location=[26.917341, 75.850471], zoom_start=12)

        # If a geojson_file is selected, add it to the map
        if geojson_file:
            geojson_path = f"data/maps/jaipur/{geojson_file}.geojson"  # Re-add extension for loading

            def style_function(feature):
                """Apply a style to the GeoJSON features."""
                return {
                    'fillColor': 'blue',
                    'color': 'black',
                    'weight': 2,
                    'fillOpacity': 0.4
                }

            # Add GeoJSON with popups for properties
            folium.GeoJson(
                geojson_path,
                name="geojson",
                style_function=style_function,
                tooltip=folium.GeoJsonTooltip(
                    fields=list(self.get_geojson_properties(geojson_path).keys()),
                    aliases=list(self.get_geojson_properties(geojson_path).keys())
                ),
                popup=folium.GeoJsonPopup(fields=list(self.get_geojson_properties(geojson_path).keys()))
            ).add_to(m)

        # Add heatmap for locations (both LADC and HADC data) after GeoJSON
        self.add_heatmap(m)

        # Add wind data visualization
        self.wind_data_visualizer.load_wind_data()  # Load wind data
        self.wind_data_visualizer.plot_wind_arrows(m)  # Plot wind arrows on the map

        # Save the map to an HTML file and load it in QWebEngineView
        m.save(self.folium_map)

        # Add custom CSS for border-radius
        self.add_custom_style()

        self.map_view.setUrl(QUrl.fromLocalFile(os.path.abspath(self.folium_map)))

    def add_custom_style(self):
        """Add custom CSS to style the map with a border radius."""
        with open(self.folium_map, 'r', encoding='utf-8') as file:
            content = file.read()

        # Add a <style> tag for border-radius
        style = """
        <style>
            .folium-map {
                border-radius: 15px;  /* Adjust the value as needed */
                overflow: hidden;  /* Prevent content overflow */
                height: 100%;  /* Ensure it fills the height */
                width: 100%;   /* Ensure it fills the width */
            }
            #map {
                border-radius: 15px;  /* Ensure map itself also has border-radius */
                overflow: hidden;
            }
        </style>
        """

        # Inject the style before the </head> tag
        content = content.replace('</head>', f'{style}</head>')

        # Write the modified content back to folium_map
        with open(self.folium_map, 'w', encoding='utf-8') as file:
            file.write(content)

    def add_heatmap(self, folium_map):
        """Add a heatmap layer to the map using the latest LADC and HADC data."""
        location_data = pd.read_csv('data/raw/LADC/__locations__.csv')
        locations = []

        for _, loc_row in location_data.iterrows():
            location_name = loc_row['location_name']
            lat = loc_row['latitude']
            lon = loc_row['longitude']

            try:
                location_file = f"data/raw/LADC/{location_name}.csv"
                ladc_data = pd.read_csv(location_file)

                # Get the last row for LADC
                if not ladc_data.empty and 'Temp' in ladc_data.columns:
                    last_row = ladc_data.iloc[-1]  # Get the last row
                    # Convert to native Python types
                    locations.append([float(lat), float(lon), float(last_row['Temp'])])
            except (FileNotFoundError, KeyError) as e:
                print(f"Error loading LADC data for {location_name}: {e}")

        # Load HADC data
        try:
            hadc_data = pd.read_csv('data/raw/HADC/location_1.csv')
            hadc_data.columns = hadc_data.columns.str.strip()

            # Get the last row for HADC
            if not hadc_data.empty and 'Temp' in hadc_data.columns:
                last_row = hadc_data.iloc[-1]  # Get the last row
                # Convert to native Python types
                locations.append([float(last_row['Latitude']), float(last_row['Longitude']), float(last_row['Temp'])])
        except (FileNotFoundError, KeyError) as e:
            print(f"Error loading HADC data: {e}")

        # Create the heatmap if there are locations
        if locations:
            HeatMap(locations, overlay=True, name='Heat Map', z_index=10).add_to(folium_map)

    def get_geojson_properties(self, geojson_path):
        """Read the GeoJSON file and return its properties for tooltips/popups."""
        with open(geojson_path, 'r', encoding='utf-8') as file:
            geojson_data = json.load(file)

        # Extract properties from the first feature as an example
        if geojson_data['features']:
            return geojson_data['features'][0]['properties']
        return {}

    def update_map_with_geojson(self):
        """Update the map when the selected GeoJSON file changes."""
        selected_geojson = self.geojson_dropdown.currentText()
        self.load_map(selected_geojson)  # Load the map with the newly selected GeoJSON

#? Main Function to Run the Application
if __name__ == "__main__":
    print("Starting the application...")  # Debug statement
    app = QApplication(sys.argv)
    window = WeatherMapApp()
    window.show()
    sys.exit(app.exec_())
