#include <ESP8266WiFi.h>
#include <Adafruit_NeoPixel.h>

#include "wifi_info.h"

/* Interface Description
 *
 * All commands arrive as raw bytes through a wifi client object
 *
 * Each packet will be formatted:
 * 1 byte - command
 * n bytes - payload, number of payload bytes depends on the command
 * 
 * Command Codes:
 * 0x00 - Turn off entire grid
 * 0x10 - Turn off entire grid - in memory only
 * 0x01 - Fill entire grid
 *        3 data bytes: [r, g, b]
 * 0x11 - Fill entire grid - in memory only
 *        3 data bytes: [r, g, b]
 * 0x02 - Fill rectangle
 *        7 data bytes: [x1, y1, x2, y2, r, g, b]
 * 0x12 - Fill rectangle - in memory only
 *        7 data bytes: [x1, y1, x2, y2, r, g, b]
 * 0x03 - Set custom
 *        data bytes: [num_leds, x1, y1, r, g, b, x2, y2, r, g, b, ...]
 * 0x13 - Set custom - in memory only
 *        data bytes: [num_leds, x1, y1, r, g, b, x2, y2, r, g, b, ...]
 * 0x0F - Show leds from memory
 * 0x80 - Set brightness
 *        1 data byte: brightness
 * 0xFF - Ping
 *        Respond with 0xFF
 */

#define GRID_PIN 4      // D2

const int port = 12321;
WiFiServer server(port);

Adafruit_NeoPixel leds(256, GRID_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(74880);
  pinMode(GRID_PIN, OUTPUT);

  Serial.println("Start");

  // Connect to the WiFi network
  Serial.printf("Connecting to %s", WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.printf(".");
  }
  Serial.println("Connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Start listening for incoming connections
  server.begin();
  Serial.printf("Listening for connections on port %d\n", port);

  // Initialize the LEDs
  leds.begin();
  leds.setBrightness(20);
  leds.clear();
  leds.show();
}

void loop() {
  WiFiClient client = server.available();
  
  if (client) {
    Serial.printf("Client connected\n");
    
    while(client.connected()) {
      if (client.available() > 0) {
        byte command = client.read();
        Serial.printf("Got command: %d\n", command);

        // Process immediate commands
        if (command == 0xFF) {
          client.write(0xFF);
          continue;
        }
        else if (command == 0x80) {
          leds.setBrightness(client.read());
          leds.show();
          continue;
        }

        // Process LED commands
        switch (command & 0xF) {
          case 0x00:
            leds.clear();
            break;
          case 0x01:
            Fill(client);
            break;
          case 0x02:
            FillRectangle(client);
            break;
          case 0x03:
            SetCustom(client);
            break;
        }

        if ((command & 0x10) == 0) {
          leds.show();
        }
      }
    }

    Serial.printf("Client disconnected\n");
  }
}

void Fill(WiFiClient& client) {
  uint8_t r = client.read();
  uint8_t g = client.read();
  uint8_t b = client.read();
  leds.fill(leds.Color(r, g, b));
}

void FillRectangle(WiFiClient& client) {
  uint8_t x1 = client.read();
  uint8_t y1 = client.read();
  uint8_t x2 = client.read();
  uint8_t y2 = client.read();
  uint8_t r = client.read();
  uint8_t g = client.read();
  uint8_t b = client.read();
  Serial.printf("filling rectangle: %d %d %d %d with color %d %d %d\n", x1, y1, x2, y2, r, g, b);
  for (uint8_t x = x1; x <= x2; ++x) {
    for (uint8_t y = y1; y <= y2; ++y) {
      leds.setPixelColor(Pixel(x, y), r, g, b);
    }
  }
}

void SetCustom(WiFiClient& client) {
  uint8_t n = client.read();
  for (uint8_t i = 0; i < n; ++i) {
    uint8_t x = client.read();
    uint8_t y = client.read();
    uint8_t r = client.read();
    uint8_t g = client.read();
    uint8_t b = client.read();
    leds.setPixelColor(Pixel(x, y), r, g, b);
  }
}

int Pixel(int x, int y) {
  int p = 16 * x;
  if (x % 2 == 0)
    return p + y;
  else
    return p + 15 - y;
}
