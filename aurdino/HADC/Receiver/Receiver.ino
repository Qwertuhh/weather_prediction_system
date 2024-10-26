#include <SPI.h>
#include <LoRa.h>

// Pin definitions for LoRa
#define SS_PIN 10
#define RST_PIN 9
#define DIO0_PIN 2

void setup() {
  Serial.begin(4800);
  
  // Initialize LoRa
  LoRa.begin(433E6);  // Set the frequency to 433 MHz
  Serial.println("LoRa Receiver Initialized");
}

void loop() {
  // Check if a packet is available
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // Read the packet
    String receivedData = "";
    while (LoRa.available()) {
      receivedData += (char)LoRa.read();
    }
    // Print received data
    Serial.println("Received: " + receivedData);
  }
}
