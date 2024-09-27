# plotting.py

import pandas as pd
import folium
from folium.plugins import HeatMap
import json

def load_map(folium_map, geojson_file=None):
    """Generate and display the map with optional GeoJSON overlay and tooltips/popups."""
    m = folium.Map(location=[26.917341, 75.850471], zoom_start=12)

    if geojson_file:
        geojson_path = f"data/maps/jaipur/{geojson_file}.geojson"

        def style_function(feature):
            return {
                'fillColor': 'blue',
                'color': 'black',
                'weight': 2,
                'fillOpacity': 0.4
            }

        folium.GeoJson(
            geojson_path,
            name="geojson",
            style_function=style_function,
            tooltip=folium.GeoJsonTooltip(
                fields=list(get_geojson_properties(geojson_path).keys()),
                aliases=list(get_geojson_properties(geojson_path).keys())
            ),
            popup=folium.GeoJsonPopup(fields=list(get_geojson_properties(geojson_path).keys()))
        ).add_to(m)

    add_heatmap(m)

    m.save(folium_map)
    return m

def add_heatmap(folium_map):
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

            if not ladc_data.empty and 'Temp' in ladc_data.columns:
                last_row = ladc_data.iloc[-1]
                locations.append([float(lat), float(lon), float(last_row['Temp'])])
        except (FileNotFoundError, KeyError) as e:
            print(f"Error loading LADC data for {location_name}: {e}")

    try:
        hadc_data = pd.read_csv('data/raw/HADC/location_1.csv')
        hadc_data.columns = hadc_data.columns.str.strip()

        if not hadc_data.empty and 'Temp' in hadc_data.columns:
            last_row = hadc_data.iloc[-1]
            locations.append([float(last_row['Latitude']), float(last_row['Longitude']), float(last_row['Temp'])])
    except (FileNotFoundError, KeyError) as e:
        print(f"Error loading HADC data: {e}")

    if locations:
        HeatMap(locations, overlay=True, name='Heat Map', z_index=10).add_to(folium_map)

def get_geojson_properties(geojson_path):
    """Read the GeoJSON file and return its properties for tooltips/popups."""
    with open(geojson_path, 'r', encoding='utf-8') as file:
        geojson_data = json.load(file)

    if geojson_data['features']:
        return geojson_data['features'][0]['properties']
    return {}
