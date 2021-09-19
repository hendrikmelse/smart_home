#pragma once

#include <ESP8266WiFi.h>
#include <queue>
#include <string>
#include <ArduinoJson.h>

class SmartHomeClient {
private:
  WiFiClient sock;
  std::queue<std::string> incoming_packets;
  
public:
  SmartHomeClient();
  bool connect(std::string addr, int port);
  bool register_device(std::string device_name);
  std::string get_devices();
  bool send_payload(std::string target, std::string payload);
  bool payload_available();
  bool get_incoming_payload(JsonDocument& doc);

private:
  std::string get_next_message();
  bool is_payload_packet(std::string packet);
};
