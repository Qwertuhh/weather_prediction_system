import pandas as pd
import folium
from folium.plugins import HeatMap
import json

def load_map(folium_map, geojson_file=None):
    """Generate and display the map with optional GeoJSON overlay and tooltips/popups."""
    # Initialize the map at the desired coordinates
    m = folium.Map(location=[26.917341, 75.850471], zoom_start=12)

    if geojson_file:
        geojson_path = f"data/maps/jaipur/{geojson_file}.geojson"

        def style_function(feature):
            return {
                'fillColor': 'grey',
                'color': 'black',
                'weight': 2,
                'fillOpacity': 0.4
            }

        try:
            # Load GeoJSON and add to the map
            folium.GeoJson(
                geojson_path,
                name="geojson",
                style_function=style_function,
                tooltip=folium.GeoJsonTooltip(
                    fields=list(get_geojson_properties(geojson_path).keys()),
                    aliases=list(get_geojson_properties(geojson_path).keys()),
                    localize=True
                ),
                popup=folium.GeoJsonPopup(
                    fields=list(get_geojson_properties(geojson_path).keys()),
                    labels=True
                )
            ).add_to(m)
        except Exception as e:
            print(f"Error loading GeoJSON file: {e}")

    add_heatmap(m)

    # Save the generated map
    folium_map_path = f"{folium_map}"
    m.save(folium_map_path)
    return m

def add_heatmap(folium_map):
    """Add a heatmap layer to the map using the latest LADC and HADC data."""
    location_data = pd.read_csv('data/raw/LADC/__locations__.csv')
    locations = []

    # Process LADC locations
    for _, loc_row in location_data.iterrows():
        location_name = loc_row['location_name']
        lat = loc_row['latitude']
        lon = loc_row['longitude']

        try:
            location_file = f"data/raw/LADC/{location_name}.csv"
            ladc_data = pd.read_csv(location_file)

            if not ladc_data.empty:
                last_row = ladc_data.iloc[-1]
                temp = float(last_row['Temp']) if 'Temp' in ladc_data.columns else 0
                humidity = float(last_row['Humidity']) if 'Humidity' in ladc_data.columns else 0
                aiq = float(last_row['AIQ']) if 'AIQ' in ladc_data.columns else 0

                # Append location data for heatmap and create a tooltip
                locations.append([float(lat), float(lon), temp])
                
                # Add a CircleMarker for LADC with tooltip
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=7,
                    color='Dark Olive Green',
                    fill=True,
                    fill_opacity=0.6,
                    popup=f"Location: {location_name}<br>Temp: {temp}°C<br>Humidity: {humidity}%<br>AIQ: {aiq}",
                    tooltip=f"{location_name}: {temp}°C"
                ).add_to(folium_map)

        except (FileNotFoundError, KeyError) as e:
            print(f"Error loading LADC data for {location_name}: {e}")

    # Process HADC locations
    try:
        hadc_data = pd.read_csv('data/raw/HADC/location_1.csv')
        hadc_data.columns = hadc_data.columns.str.strip()

        if not hadc_data.empty:
            for _, hadc_row in hadc_data.iterrows():
                temp = float(hadc_row['Temp']) if 'Temp' in hadc_data.columns else 0
                humidity = float(hadc_row['Humidity']) if 'Humidity' in hadc_data.columns else 0
                aiq = float(hadc_row['AIQ']) if 'AIQ' in hadc_data.columns else 0
                lat = float(hadc_row['Latitude'])
                lon = float(hadc_row['Longitude'])

                # Add a CircleMarker for HADC with tooltip
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=7,
                    color='Steel Blue',
                    fill=True,
                    fill_opacity=0.6,
                    popup=f"HADC<br>Temp: {temp}°C<br>Humidity: {humidity}%<br>AIQ: {aiq}",
                    tooltip=f"HADC: {temp}°C"
                ).add_to(folium_map)

                locations.append([lat, lon, temp])
    except (FileNotFoundError, KeyError) as e:
        print(f"Error loading HADC data: {e}")

    # Add heatmap layer for LADC and HADC
    if locations:
        HeatMap(locations, overlay=True, name='Heat Map', z_index=10).add_to(folium_map)

def get_geojson_properties(geojson_path):
    """Read the GeoJSON file and return its properties for tooltips/popups."""
    with open(geojson_path, 'r', encoding='utf-8') as file:
        geojson_data = json.load(file)

    if geojson_data['features']:
        return geojson_data['features'][0]['properties']
    return {}
