import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Initialize parameters
start_time = datetime(2024, 9, 23, 21, 11)
num_entries = 10  # Number of entries to generate
initial_temp = 30  # Starting temperature
initial_humi = 70   # Humidity
initial_aiq = 45    # Air Quality Index
initial_height = 433 # Height
initial_latitude = 26.916974494976014  # Starting latitude
initial_longitude = 75.85001155326638  # Starting longitude

# Prepare lists to hold the generated data
times = []
temps = []
humis = []
aiqs = []
heights = []
latitudes = []
longitudes = []

# Generate data
for i in range(num_entries):
    # Increment time
    current_time = start_time + timedelta(minutes=i * 2)  # Increment by 10 minutes
    times.append(current_time.strftime('%Y-%m-%d %H:%M'))

    # Gradual decrease in temperature
    current_temp = initial_temp - i * 2  # Decrease temperature by 2 degrees
    temps.append(current_temp)

    # Keeping humidity and AIQ constant for this example
    humis.append(initial_humi - i * (i**0.1))
    aiqs.append(initial_aiq - i * 1.2)

    # Gradual change in height (arbitrarily chosen, slight increase)
    heights.append(initial_height + i)  # Increase height by 1 meter

    # Gradual increment in coordinates (arbitrarily chosen small increments)
    latitudes.append(initial_latitude + i * 0.005)  # Increment latitude
    longitudes.append(initial_longitude + i * 0.0009)  # Increment longitude

# Create a DataFrame
data = {
    "Time": times,
    "Temp": temps,
    "Humi": humis,
    "AIQ": aiqs,
    "Height": heights,
    "Latitude": latitudes,
    "Longitude": longitudes,
}

df = pd.DataFrame(data)

# Save to CSV
csv_file_path = 'data/raw/HADC/location_1.csv'
df.to_csv(csv_file_path, index=False)

csv_file_path
