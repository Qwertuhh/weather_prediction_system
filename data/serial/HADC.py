import serial
import time

ser = serial.Serial('COM7', 9600, timeout=1) 
time.sleep(2)  # Allow time for the connection to establish

# Open a file to store the data
with open('data.csv', 'w') as file:
    file.write('Temperature,Humidity\n')  # Write header

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()  # Read a line from the serial port
            if line:  # If there's data
                print(line)  # Print the line to the console
                # Split the line to extract temperature and humidity
                parts = line.split(',')
                if len(parts) == 2:
                    temp = parts[0].split(':')[1].strip()
                    hum = parts[1].split(':')[1].strip()
                    file.write(f"{temp},{hum}\n")  # Write data to the file

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()  # ? Close the serial port when done
