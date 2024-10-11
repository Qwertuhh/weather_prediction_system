import pandas as pd
import folium
import numpy as np
from folium.plugins import HeatMap
import json
from branca.colormap import LinearColormap
from .wind_engine import WindEngine

class MapVisualization:
    def __init__(self, ladc_file, hadc_file, is_dark_mode):
        self.ladc_file = ladc_file
        self.hadc_file = hadc_file
        self.is_dark_mode = is_dark_mode
        self.wind_map = folium.Map(location=[26.917341, 75.850471], zoom_start=12, 
                                   tiles='cartodbdark_matter' if is_dark_mode else 'cartodbpositron')

    def load_ladc_data(self):
        try:
            return pd.read_csv(self.ladc_file)
        except FileNotFoundError:
            print(f"Error: File {self.ladc_file} not found.")
            return None

    def load_hadc_data(self):
        try:
            return pd.read_csv(self.hadc_file)
        except FileNotFoundError:
            print(f"Error: File {self.hadc_file} not found.")
            return None

    def add_heatmap_and_circle_markers(self):
        ladc_data = self.load_ladc_data()
        if ladc_data is not None:
            heat_data = []
            for _, loc_row in ladc_data.iterrows():
                location_name = loc_row['location_name']
                lat = loc_row['latitude']
                lon = loc_row['longitude']
                temperature = loc_row.get('temperature', 25)

                heat_data.append([lat, lon, temperature])

                folium.CircleMarker(
                    location=(lat, lon),
                    radius=8,
                    color='#4A90E2',
                    fill=True,
                    fill_color='#4A90E2',
                    fill_opacity=0.7,
                    popup=f"{location_name}: {temperature}°C"
                ).add_to(self.wind_map)

            HeatMap(heat_data, radius=20, blur=15, max_zoom=1, 
                    gradient={0.4: '#87CEFA', 0.65: '#4A90E2', 1: '#0000FF'}).add_to(self.wind_map)

        hadc_data = self.load_hadc_data()
        if hadc_data is not None:
            heat_data_hadc = []
            for _, hadc_row in hadc_data.iterrows():
                lat = hadc_row['Latitude']
                lon = hadc_row['Longitude']
                temperature = hadc_row.get('Temp', 25)

                heat_data_hadc.append([lat, lon, temperature])

                folium.CircleMarker(
                    location=(lat, lon),
                    radius=8,
                    color='#FF6B6B',
                    fill=True,
                    fill_color='#FF6B6B',
                    fill_opacity=0.7,
                    popup=f"Temp: {temperature}°C at ({lat}, {lon})"
                ).add_to(self.wind_map)

            HeatMap(heat_data_hadc, radius=20, blur=15, max_zoom=1, 
                    gradient={0.4: '#FFA07A', 0.65: '#FF6B6B', 1: '#DC143C'}).add_to(self.wind_map)

    def add_wind_arrows_and_markers(self):
        ladc_data = self.load_ladc_data()
        if ladc_data is not None:
            for _, loc_row in ladc_data.iterrows():
                lat = loc_row['latitude']
                lon = loc_row['longitude']
                wind_direction = WindEngine.calculate_wind_direction(loc_row.get('temperature', 25))

                folium.Marker(
                    location=[lat, lon],
                    icon=folium.DivIcon(html=f'<div style="color: #4A90E2; font-size: 20px; transform: rotate({wind_direction}deg);">➤</div>')
                ).add_to(self.wind_map)

        hadc_data = self.load_hadc_data()
        if hadc_data is not None:
            for _, hadc_row in hadc_data.iterrows():
                lat = hadc_row['Latitude']
                lon = hadc_row['Longitude']
                wind_direction = WindEngine.calculate_wind_direction(hadc_row.get('Temp', 25))

                folium.Marker(
                    location=[lat, lon],
                    icon=folium.DivIcon(html=f'<div style="color: #FF6B6B; font-size: 20px; transform: rotate({wind_direction}deg);">➤</div>')
                ).add_to(self.wind_map)

    def display_map(self):
        return self.wind_map

    @staticmethod
    def create_wind_map(ladc_file, hadc_file, geojson_file=None, is_dark_mode=False):
        wind_visualizer = MapVisualization(ladc_file, hadc_file, is_dark_mode)
        wind_visualizer.add_heatmap_and_circle_markers()
        wind_visualizer.add_wind_arrows_and_markers()

        if geojson_file:
            wind_visualizer.load_geojson(geojson_file)

        wind_visualizer.display_map().save('plots/components/html/folium.html')

    def load_geojson(self, geojson_file):
        geojson_path = f"data/maps/jaipur/{geojson_file}.geojson"

        colormap = LinearColormap(colors=['#E0E0E0', '#C0C0C0', '#A0A0A0'], vmin=0, vmax=100)
        
        def style_function(feature):
            return {
                'fillColor': colormap(feature['properties'].get('value', 50)),
                'color': '#808080',
                'weight': 1,
                'fillOpacity': 0.3
            }

        geojson_layer = folium.GeoJson(
            geojson_path,
            name="geojson",
            style_function=style_function,
            tooltip=folium.GeoJsonTooltip(
                fields=list(self.get_geojson_properties(geojson_path).keys()),
                aliases=list(self.get_geojson_properties(geojson_path).keys()),
                style=("background-color: rgba(46, 46, 46, 0.8); color: #FFFFFF; font-family: arial; font-size: 12px; padding: 10px;") if self.is_dark_mode else ("background-color: rgba(255, 255, 255, 0.8); color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
            ),
            popup=folium.GeoJsonPopup(fields=list(self.get_geojson_properties(geojson_path).keys()))
        )
        
        geojson_layer.add_to(self.wind_map)
        colormap.add_to(self.wind_map)

    @staticmethod
    def get_geojson_properties(geojson_path):
        with open(geojson_path, 'r', encoding='utf-8') as file:
            geojson_data = json.load(file)

        if geojson_data['features']:
            return geojson_data['features'][0]['properties']
        return {}