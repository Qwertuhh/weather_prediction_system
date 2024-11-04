import serial
import time
import os
import csv

# Function to create a directory for storing the data file
def create_directory():
    top_dir = os.path.join(os.getcwd(), "data/raw/HADC")
    if not os.path.exists(top_dir):
        os.makedirs(top_dir)
    return top_dir

# Function to save data to a CSV file
def save_data_to_csv(data, file_path):
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Serial port configuration
port = 'COM8'
baud_rate = 4800
timeout = 1

# Fixed location values for the test
height = 433
latitude = 26.916974494976014
longitude = 75.85001155326638

# Setup the directory and CSV file
directory = create_directory()
file_path = os.path.join(directory, "location_2.csv")

# Setup serial connection
ser = serial.Serial(port, baud_rate, timeout=timeout)

# Create the CSV file and write the header if it doesn't exist
if not os.path.exists(file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Temp", "Humi", "AIQ", "Height", "Latitude", "Longitude"])

print("Reading from serial port...")

# Function to clean up corrupted data (e.g., remove unexpected characters)
def clean_data(data):
    # Remove any unwanted leading characters and 'Received: ' prefix
    if "Received: " in data:
        data = data.replace("Received: ", "").strip()
    return data

# Function to validate the values
def is_valid_data(temp, humidity, aq):
    # Define reasonable ranges for each of the sensor values
    return (0 <= temp <= 100) and (0 <= humidity <= 100) and (0 <= aq <= 1000)

try:
    while True:
        # Read data from the serial port
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print(f"Raw Received: {data}")
            
            # Clean up the data
            data = clean_data(data)

            # Ignore any empty or incomplete lines
            if not data or len(data.split()) < 3:
                print(f"Skipping invalid data: {data}")
                continue

            print(f"Cleaned Data: {data}")

            # Split the data into parts (assuming format "T:xx.x H:xx.x AQ:xxx")
            try:
                data_parts = data.split()  # Split by space to extract each part
                
                temp_str = data_parts[0][2:]  # Extract temperature value (after "T:")
                humidity_str = data_parts[1][2:]  # Extract humidity value (after "H:")
                aq_str = data_parts[2][3:]  # Extract AQ value (after "AQ:")

                # Convert the strings to floats
                temp = float(temp_str)
                humidity = float(humidity_str)
                aq = float(aq_str)

                # Validate the extracted data to avoid storing unrealistic values
                if not is_valid_data(temp, humidity, aq):
                    print(f"Invalid data detected (out of bounds): {data}")
                    continue

                # Get the current timestamp
                timestamp = time.strftime("%Y-%m-%d %H:%M")

                # Save the data to the CSV file
                save_data_to_csv([timestamp, temp, humidity, aq, height, latitude, longitude], file_path)
                print(f"Data saved: {timestamp}, {temp}, {humidity}, {aq}")
            except (IndexError, ValueError) as e:
                print(f"Error parsing data: {data}, Error: {e}")
            
        # Sleep for a short time to prevent overloading the CPU
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nStopped by user.")
finally:
    ser.close()
    print("Serial connection closed.")
