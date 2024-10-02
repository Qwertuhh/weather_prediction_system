import pandas as pd
import folium
import numpy as np
from folium.plugins import HeatMap

class WindDataVisualizer:
    def __init__(self, ladc_file, hadc_file):
        self.ladc_file = ladc_file
        self.hadc_file = hadc_file
        self.wind_map = folium.Map(location=[26.917341, 75.850471], zoom_start=12)

    def load_ladc_data(self):
        """Load LADC data from the CSV file."""
        try:
            return pd.read_csv(self.ladc_file)
        except FileNotFoundError:
            print(f"Error: File {self.ladc_file} not found.")
            return None

    def load_hadc_data(self):
        """Load HADC data from the CSV file."""
        try:
            return pd.read_csv(self.hadc_file)
        except FileNotFoundError:
            print(f"Error: File {self.hadc_file} not found.")
            return None

    def calculate_wind_direction(self, temperature):
        """Calculate wind direction based on temperature."""
        if temperature < 20:
            return 270  # Wind from West
        elif temperature < 30:
            return 0    # Wind from East
        else:
            return 90   # Wind from North

    def add_heatmap_and_circle_markers(self):
        """Add heatmap and circle markers for LADC and HADC data."""
        # Load LADC data
        ladc_data = self.load_ladc_data()
        if ladc_data is not None:
            heat_data = []
            for _, loc_row in ladc_data.iterrows():
                location_name = loc_row['location_name']
                lat = loc_row['latitude']
                temperature = loc_row.get('temperature', 25)

                # Add to heatmap data
                heat_data.append([lat, loc_row['longitude'], temperature])

                # Add circle marker for LADC
                folium.CircleMarker(
                    location=(lat, loc_row['longitude']),
                    radius=8,
                    color='blue',
                    fill=True,
                    fill_color='blue',
                    fill_opacity=0.6,
                    popup=f"{location_name}: {temperature}°C"
                ).add_to(self.wind_map)

            # Create heatmap layer for LADC
            HeatMap(heat_data, radius=15).add_to(self.wind_map)

        # Load HADC data
        hadc_data = self.load_hadc_data()
        if hadc_data is not None:
            heat_data_hadc = []
            for _, hadc_row in hadc_data.iterrows():
                lat = hadc_row['Latitude']
                lon = hadc_row['Longitude']
                temperature = hadc_row.get('Temp', 25)  # Default temperature if not found

                # Add to heatmap data
                heat_data_hadc.append([lat, lon, temperature])

                # Add circle marker for HADC
                folium.CircleMarker(
                    location=(lat, lon),
                    radius=8,
                    color='red',
                    fill=True,
                    fill_color='red',
                    fill_opacity=0.6,
                    popup=f"Temp: {temperature}°C at ({lat}, {lon})"
                ).add_to(self.wind_map)

            # Create heatmap layer for HADC
            HeatMap(heat_data_hadc, radius=15).add_to(self.wind_map)

    def add_wind_arrows_and_markers(self):
        """Add wind direction arrows to the map with only arrowhead at the tail (starting point)."""
        # Load LADC data
        ladc_data = self.load_ladc_data()
        if ladc_data is not None:
            for _, loc_row in ladc_data.iterrows():
                location_name = loc_row['location_name']
                lat = loc_row['latitude']
                lon = loc_row['longitude']
                wind_direction = self.calculate_wind_direction(loc_row.get('temperature', 25))

                # Calculate the position for the arrowhead (just for the tail position)
                arrow_length = 0.005  # You can adjust this to control the direction length for the arrowhead
                end_lat = lat + arrow_length * np.sin(np.radians(wind_direction))
                end_lon = lon + arrow_length * np.cos(np.radians(wind_direction))

                # Add arrowhead marker only at the starting point
                folium.Marker(
                    location=[lat, lon],  # Plot at the starting location (tail)
                    icon=folium.DivIcon(html='<div style="color: Pale Turquoise; font-size: 16px;">&#8599;</div>')  # Arrowhead
                ).add_to(self.wind_map)

        # Load HADC data
        hadc_data = self.load_hadc_data()
        if hadc_data is not None:
            for _, hadc_row in hadc_data.iterrows():
                lat = hadc_row['Latitude']
                lon = hadc_row['Longitude']
                wind_direction = self.calculate_wind_direction(hadc_row.get('Temp', 25))

                # Calculate the position for the arrowhead (just for the tail position)
                arrow_length = 0.005  # You can adjust this for the arrowhead
                end_lat = lat + arrow_length * np.sin(np.radians(wind_direction))
                end_lon = lon + arrow_length * np.cos(np.radians(wind_direction))

                # Add arrowhead marker only at the starting point
                folium.Marker(
                    location=[lat, lon],  # Plot at the starting location (tail)
                    icon=folium.DivIcon(html='<div style="color: orchid; font-size: 16px;">&#8599;</div>')  # Arrowhead
                ).add_to(self.wind_map)


    def display_map(self):
        """Display the Folium map."""
        return self.wind_map

    @staticmethod
    def create_wind_map(ladc_file, hadc_file):
        """Create and display the wind map."""
        wind_visualizer = WindDataVisualizer(ladc_file, hadc_file)
        wind_visualizer.add_heatmap_and_circle_markers()  # Add heatmap and markers
        wind_visualizer.add_wind_arrows_and_markers()     # Add arrows

        # Save the map to an HTML file
        wind_visualizer.display_map().save('plots/components/html/folium.html')


# Run the function to create the map
if __name__ == "__main__":
    ladc_path = 'data/raw/LADC/__locations__.csv'
    hadc_path = 'data/raw/HADC/Location_1.csv'
    WindDataVisualizer().create_wind_map(ladc_path, hadc_path)
