#include <ESP8266WiFi.h>
#include <Adafruit_NeoPixel.h>
#include <string>
#include <string.h>
#include "smart_home_client.h"

// Doing this so I can .gitignore wifi_info.h
// wifi_info.h #defines WIFI_SSID and WIFI_PASSWORD
#include "wifi_info.h"

#define LED_PIN 5
#define STRIP_PIN 4

#define LED_COUNT 60

std::string host = "192.168.1.33";
const int port = 42069;

SmartHomeClient shClient;

StaticJsonDocument<1024> doc;
Adafruit_NeoPixel strip(LED_COUNT, STRIP_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  pinMode(STRIP_PIN, OUTPUT);
  for (int i = 0; i < 5; ++i) {
    digitalWrite(LED_PIN, HIGH);
    delay(100);
    digitalWrite(LED_PIN, LOW);
    delay(100);
  }
  Serial.printf("\n");

  Serial.printf("Connecting to %s", WIFI_SSID);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.printf(".");
  }

  Serial.printf("Connected\n");

  Serial.printf("Connecting smart home client...\n");
  shClient.connect(host, port);
  Serial.printf("Connected\n");
  shClient.register_device("led_strip");

  strip.begin();
  strip.setBrightness(20);
  strip.clear();
  strip.show();
}

void loop() {
  if (shClient.payload_available()) {
    shClient.get_incoming_payload(doc);
    const char* sender = doc["sender"];
    const char* payload = doc["payload"];
    Serial.printf("Sender: %s\n", sender);
    Serial.printf("Payload: %s\n", payload);
    Serial.println();

    if (strcmp(payload, "on") == 0) {
      strip.fill(strip.Color(128, 0, 255));
      strip.show();
    }
    else if (strcmp(payload, "off") == 0) {
      strip.clear();
      strip.show();
    }
  }
}
