#include <SPI.h>
#include <LoRa.h>

// Pin definitions for LoRa
#define SS_PIN 10
#define RST_PIN 9
#define DIO0_PIN 2

// Sensor pins
#define MQ135_PIN A0  // Air quality sensor
#define TEMP_PIN A1   // Temperature sensor (example pin)
#define HUMI_PIN A2   // Humidity sensor (example pin)

void setup() {
  Serial.begin(9600);
  
  // Initialize LoRa
  LoRa.begin(433E6);  // Set the frequency to 433 MHz
  Serial.println("LoRa Sender Initialized");
}

void loop() {
  // Read sensor values
  float airQuality = analogRead(MQ135_PIN);
  float temperature = analogRead(TEMP_PIN); // Replace with actual temperature reading logic
  float humidity = analogRead(HUMI_PIN);    // Replace with actual humidity reading logic

  // Format data as a string
  String data = "T:" + String(temperature) + " H:" + String(humidity) + " AQ:" + String(airQuality);
  
  // Send data
  LoRa.beginPacket();
  LoRa.print(data);
  LoRa.endPacket();
  
  Serial.println("Sent: " + data);
  
  // Delay before sending the next packet
  delay(2000); // Adjust the delay as necessary
}
