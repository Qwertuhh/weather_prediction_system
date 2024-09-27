#include <DHT.h>

// Define the pin where the DHT11 is connected
#define DHTPIN 2

// Define the type of DHT sensor
#define DHTTYPE DHT11

// Create a DHT object
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  // Start the serial communication
  Serial.begin(9600);
  // Initialize the DHT sensor
  dht.begin();
  pinMode(13,OUTPUT);
}

void loop() {
  // Wait a few seconds between measurements
  digitalWrite(13,HIGH);
  delay(2000);
  // Read temperature as Celsius
  float temperature = dht.readTemperature();
  // Read humidity
  float humidity = dht.readHumidity();

  // Check if any reads failed and exit early
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Print the values to the Serial Monitor
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" °C, Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");

  digitalWrite(13,LOW); // ?  To Blink (Off)
}
