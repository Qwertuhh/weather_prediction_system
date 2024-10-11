import pandas as pd
import time
import serial
from datetime import datetime
import os

# Initialize an empty DataFrame with the required columns
columns = ['Time', 'Temp', 'Humi', 'AIQ']
data = pd.DataFrame(columns=columns)

# File to save the data
file_name = 'data/raw/LADC/location_4.csv'

# Create the directory if it doesn't exist
os.makedirs(os.path.dirname(file_name), exist_ok=True)

# Check for write permission in the directory
if not os.access(os.path.dirname(file_name), os.W_OK):
    print(f"No write permission for directory: {os.path.dirname(file_name)}")
    exit(1)  # Exit the program if there is no permission

# Set up the serial connection (adjust COM port as necessary)
try:
    ser = serial.Serial('COM7', 9600, timeout=1)
    time.sleep(2)  # Allow time for the connection to establish
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

# Function to read from serial and save data to CSV
def read_and_save_data():
    global data
    line = ser.readline().decode('utf-8').strip()  # Read a line from the serial port

    if line:  # If there's data
        print(f"Raw data: {line}")  # Debug print to check what is being read

        # Assuming the expected format: Temperature: XX.XX °C  Humidity: XX.XX %  Air Quality Value: XX
        parts = line.split('\t')  # Split by tab character

        # Check if the expected parts are present
        if len(parts) == 3:
            try:
                # Extract values
                temp = float(parts[0].split(':')[1].strip().split()[0])  # Get numeric part
                humi = float(parts[1].split(':')[1].strip().split()[0])  # Get numeric part
                air_quality = int(parts[2].split(':')[1].strip())  # Get air quality value
                
                # Get the current timestamp
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M')

                # Create a new row of data
                new_data = pd.DataFrame([[current_time, temp, humi, air_quality]], columns=columns)

                # Concatenate the new data
                data = pd.concat([data, new_data], ignore_index=True)

                # Save the DataFrame to CSV
                data.to_csv(file_name, index=False)
                print(f"Data saved: {current_time}, {temp}, {humi}, {air_quality}")  # Confirmation print

            except ValueError as ve:
                print(f"Value error: {ve}")
            except Exception as e:
                print(f"Error processing data: {e}")

# Main execution loop
if __name__ == '__main__':
    print('Press Ctrl+C to stop the data collection')
    try:
        while True:
            read_and_save_data()
            time.sleep(2)  # Wait for 2 seconds before the next update
    except KeyboardInterrupt:
        print('\nData collection stopped.')
        print('Current data saved in', file_name)
    finally:
        ser.close()  # Close the serial port when done
