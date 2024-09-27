import pandas as pd
import folium
from folium.plugins import HeatMap

class WindDataVisualizer:
    def __init__(self, ladc_locations_path, hadc_data_path):
        self.ladc_locations_path = ladc_locations_path
        self.hadc_data_path = hadc_data_path
        self.wind_data = []  # To store wind data for plotting

    def load_wind_data(self):
        """Load LADC locations and HADC data to create wind visualization."""
        location_data = pd.read_csv(self.ladc_locations_path)
        locations = []

        for _, loc_row in location_data.iterrows():
            location_name = loc_row['location_name']
            lat = loc_row['latitude']
            lon = loc_row['longitude']

            try:
                location_file = f"data/raw/LADC/{location_name}.csv"
                ladc_data = pd.read_csv(location_file)

                # Get the last row for LADC
                if not ladc_data.empty:
                    last_row = ladc_data.iloc[-1]  # Get the last row
                    # Add wind data (assuming wind speed and direction are present)
                    wind_speed = last_row['Wind_Speed'] if 'Wind_Speed' in ladc_data.columns else 0
                    wind_direction = last_row['Wind_Direction'] if 'Wind_Direction' in ladc_data.columns else 0

                    locations.append((lat, lon, wind_speed, wind_direction))  # Store lat, lon, wind speed and direction
            except (FileNotFoundError, KeyError) as e:
                print(f"Error loading LADC data for {location_name}: {e}")

        # Load HADC data for wind visualization
        try:
            hadc_data = pd.read_csv(self.hadc_data_path)
            if not hadc_data.empty:
                for _, hadc_row in hadc_data.iterrows():
                    # Assuming similar structure for HADC data
                    lat = hadc_row['Latitude']
                    lon = hadc_row['Longitude']
                    wind_speed = hadc_row['Wind_Speed'] if 'Wind_Speed' in hadc_data.columns else 0
                    wind_direction = hadc_row['Wind_Direction'] if 'Wind_Direction' in hadc_data.columns else 0
                    locations.append((lat, lon, wind_speed, wind_direction))  # Store lat, lon, wind speed and direction
        except (FileNotFoundError, KeyError) as e:
            print(f"Error loading HADC data: {e}")

        self.wind_data = locations

    def plot_wind_arrows(self, folium_map):
        """Plot wind arrows on the Folium map."""
        for lat, lon, wind_speed, wind_direction in self.wind_data:
            # Calculate arrow length based on wind speed
            arrow_length = wind_speed * 0.01  # Scale factor for arrow length
            arrow_color = 'blue'  # Arrow color
            
            # Create a folium marker for each wind location
            folium.Marker(location=[lat, lon]).add_to(folium_map)

            # Calculate end point for arrow based on wind direction
            end_lat = lat + (arrow_length * (wind_direction / 360.0))  # Basic direction calculation
            end_lon = lon + (arrow_length * (wind_direction / 360.0))  # Basic direction calculation

            # Draw the wind arrow
            folium.PolyLine(
                locations=[[lat, lon], [end_lat, end_lon]],
                color=arrow_color,
                weight=2.5,
                opacity=0.8,
            ).add_to(folium_map)

    def visualize(self):
        """Create a map and plot wind data."""
        self.load_wind_data()  # Load wind data
        # Create a base Folium map
        m = folium.Map(location=[26.917341, 75.850471], zoom_start=12)
        self.plot_wind_arrows(m)  # Plot wind arrows on the map
        return m
