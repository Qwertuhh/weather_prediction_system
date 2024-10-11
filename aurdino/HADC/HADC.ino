#include <DHT.h>

#define DHTPIN 2        // Pin where the DHT11 data pin is connected
#define DHTTYPE DHT11   // Define the type of sensor (DHT11)
#define MQ135_PIN A0    // Pin where the MQ-135 analog output is connected

DHT dht(DHTPIN, DHTTYPE); // Create an instance of the DHT class

void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud
  dht.begin();        // Initialize the DHT sensor
}

void loop() {
  delay(2000); // Wait for 2 seconds between readings

  // Read DHT11 Sensor Data
  float humidity = dht.readHumidity();    // Read humidity
  float temperature = dht.readTemperature(); // Read temperature in Celsius

  // Check if any reads failed and exit early (to try again).
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Read MQ-135 Sensor Data
  int mq135Value = analogRead(MQ135_PIN); // Read analog value from MQ-135

  // Print the results to the Serial Monitor
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" °C\t");
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.print(" %\t"); 
  Serial.print("\tAir Quality Value: ");
  Serial.println(mq135Value); // Print the raw MQ-135 value
}
