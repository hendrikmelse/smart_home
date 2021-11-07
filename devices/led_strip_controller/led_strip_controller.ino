#include <ESP8266WiFi.h>
#include <Adafruit_NeoPixel.h>

// Doing this so I can .gitignore wifi_info.h
// wifi_info.h defines constant macros WIFI_SSID and WIFI_PASSWORD
#include "wifi_info.h"

#include "Bouncer.h"

/* Protocol
 * Listen for commands coming in over WiFi
 * Data will be formatted as:
 * 1 byte: command
 * n bytes: data, number of bytes depends on command
 * 
 * Note that messages cannot be longer than 256 bytes total
 * 
 * Command codes are
 * 0x00 - turn entire strip off
 * 0x10 - turn strip off in memory, but don't show on the leds
 * 0x01 - turn entire strip on
 *        3 data bytes: [r, g, b]
 * 0x11 - turn entire strip on, but don't show on the leds
 *        3 data bytes: [r, g, b]
 * 0x02 - fill a portion of the strip
 *        5 data bytes: [start, end, r, g, b]
 * 0x12 - fill a portion of the strip, but don't show on the leds
 *        5 data bytes: [start, end, r, g, b]
 * 0x03 - set leds custom
 *        data bytes: [num_indicies, index, r, g, b, index, r, g, b...]
 * 0x13 - set leds custom, but don't show on the leds
 *        data bytes: [num_indicies, index, r, g, b, index, r, g, b...]
 * 0x0F - show the leds
 * 0x20 - revert to idle animation
 * 0x80 - set the brghtness
 *        1 data byte: brightness
 * 0xFF - ping
 *        device responds with 0xFF
 */

#define LED_PIN 5     // D1
#define STRIP_PIN 4   // D2

#define LED_COUNT 60

const int port = 12321;
WiFiServer server(port);

Adafruit_NeoPixel strip(LED_COUNT, STRIP_PIN, NEO_GRB + NEO_KHZ800);

const unsigned long frame_time_micros = 7000;
unsigned long last_frame_time = 0;

bool idling = false;
Bouncer bouncer(&strip);

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  pinMode(STRIP_PIN, OUTPUT);

  // Flash the LED to indicate program start
  for (int i = 0; i < 5; ++i) {
    digitalWrite(LED_PIN, HIGH);
    delay(50);
    digitalWrite(LED_PIN, LOW);
    delay(50);
  }
  Serial.printf("\n");

  // Connect to the WiFi network
  Serial.printf("Connecting to %s", WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.printf(".");
  }
  Serial.printf("Connected\n");
  Serial.printf("IP address: ");
  Serial.println(WiFi.localIP());

  // Start listening for incoming connections
  server.begin();
  Serial.printf("Listening for connections on port %d\n", port);

  // Initialize the LED strip
  strip.begin();
  strip.setBrightness(20);
  strip.clear();
  strip.show();

  last_frame_time = micros();
}

void loop() {
  WiFiClient client = server.available();

  if (client) {
    Serial.printf("Client connected\n");
    while (client.connected()) {
      if (client.available() > 0) {
        byte command = client.read();
        Serial.printf("Got command: %d\n", command);
        
        if (command == 0xFF) {
          client.write(0xFF);
          continue
        }
        else if (command == 0x80) {
          strip.setBrightness(client.read());
          strip.show();
          continue;
        }
        else if (command == 0x20) {
          idling = true;
          continue;
        }
        else {
          idling = false;
        }

        switch(command & 0xF) {
          case 0x0:
            strip.clear();
            break;
          case 0x1:
            Fill(client);
            break;
          case 0x2:
            FillPortion(client);
            break;
          case 0x3:
            Custom(client);
            break;
        }

        if ((command & 0x10) == 0) {
          strip.show();
        }
      }

      if (idling) {
        while ((unsigned long)(micros() - last_frame_time) < frame_time_micros);
        last_frame_time = micros();
        
        strip.clear();
        bouncer.Next();
        strip.show();
      }
    }
    Serial.printf("Client disconnected\n");
  }
}

void Fill(WiFiClient& client) {
  byte r = client.read();
  byte g = client.read();
  byte b = client.read();
  strip.fill(strip.Color(r, g, b));
}

void FillPortion(WiFiClient& client) {
  byte start = client.read();
  byte end = client.read();
  byte r = client.read();
  byte g = client.read();
  byte b = client.read();
  Serial.printf("filling portion from %d to %d with %d, %d, %d\n", start, end, r, g, b);
  strip.fill(strip.Color(r, g, b), start, end - start);
}

void Custom(WiFiClient& client) {
  for (byte remaining_indicies = client.read(); remaining_indicies > 0; --remaining_indicies) {
    byte index = client.read();
    byte r = client.read();
    byte g = client.read();
    byte b = client.read();
    strip.setPixelColor(index, strip.Color(r, g, b));
  }
}

/*void advance_idle_frame() {
  while ((unsigned long)(micros() - last_frame_time) < idle_frame_time);
  
  strip.clear();
  
}*/
