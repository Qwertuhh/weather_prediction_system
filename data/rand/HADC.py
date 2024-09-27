import pandas as pd
import time
from datetime import datetime
import random

# Initialize an empty DataFrame with the required columns
columns = ['Time', 'Temp', 'Humi', 'AIQ', 'Height', 'Latitude', 'Longitude']
data = pd.DataFrame(columns=columns)

# File to save the data
file_name = 'data/raw/HADC/location_1.csv'

# Latitude and Longitude seed values
base_latitude = 26.917341
base_longitude = 75.850471

# Function to generate real-time data
def generate_data():
    global data
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # Simulated sensor data
    temp = random.randint(29, 35)        # Temperature in °C
    humi = random.randint(60, 75)        # Humidity in %
    aiq = random.randint(35, 50)         # Air Quality Index
    height = random.randint(100, 500)    # Altitude in meters
    latitude = base_latitude + random.uniform(-0.001, 0.001)
    longitude = base_longitude + random.uniform(-0.001, 0.001)
    
    # ? Create a new row of data
    new_data = pd.DataFrame([[current_time, temp, humi, aiq, height, latitude, longitude]], columns=columns)
    
    # ? Concatenate only if data is not empty
    if data.empty:
        data = new_data  # If empty, directly assign the new data
    else:
        data = pd.concat([data, new_data], ignore_index=True)
    
    # ? Save the DataFrame to CSV
    data.to_csv(file_name, index=False)
    

# ? Generate real-time data at 2-second intervals
if __name__ == '__main__':
    print('Press Ctrl+C to stop the simulation')
    try:
        while True:
            generate_data()
            time.sleep(2)  # Wait for 2 seconds before the next update
    except KeyboardInterrupt:
        print('\nSimulation stopped.')
        print('Current data saved in', file_name)
