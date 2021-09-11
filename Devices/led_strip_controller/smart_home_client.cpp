#include "smart_home_client.h"

SmartHomeClient::SmartHomeClient() {
}

bool SmartHomeClient::connect(std::string addr, int port) {
  Serial.printf("Connecting to %s:%d... ", addr.c_str(), port);
  if (this->sock.connect(addr.c_str(), port)) {
    Serial.printf("Connected\n");
    return true;
  }
  else {
    Serial.printf("Failed\n");
    return false;
  }
}

bool SmartHomeClient::register_device(std::string device_name) {
  StaticJsonDocument<1024> doc;
  doc["target"] = "server";
  JsonObject payload = doc.createNestedObject("payload");
  payload["command"] = "register";
  payload["device_name"] = device_name;
  payload["force"] = true;

  std::string s;
  serializeJson(doc, s);

  this->sock.write(s.c_str());
  delay(500);

  s = this->get_next_message();
  Serial.printf("Got response: %s\n", s.c_str());
  return true;
}

bool SmartHomeClient::payload_available() {
  if (!this->incoming_packets.empty()) {
    return true;
  }

  std::string s = this->get_next_message();

  if (s == "") {
    return false;
  }
  else {
    this->incoming_packets.push(s);
    return true;
  }
}

bool SmartHomeClient::get_incoming_payload(JsonDocument& doc) {
  if (!this->payload_available()) {
    return false;
  }

  std::string s = this->incoming_packets.front();
  this->incoming_packets.pop();

  DeserializationError error = deserializeJson(doc, s.c_str());

  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.f_str());
    return false;
  }
  
  return true;
}

// Get the next message from the socket
std::string SmartHomeClient::get_next_message() {
  if (!this->sock.available()) {
    return "";
  }

  char c = this->sock.read();
  if (c != '{') {
    this->sock.flush();
    Serial.printf("Error: Incoming message did not start with '{'\n");
    return "";
  }

  std::string s = "{";
  int num_braces = 1;

  while (this->sock.available()) {
    c = this->sock.read();
    s += c;
    if (c == '{') {
      num_braces++;
    }
    if (c == '}') {
      num_braces--;
    }

    if (num_braces == 0) {
      return s;
    }
  }

  Serial.printf("Error: Incoming message did not have the same number of opening and closing braces\n");
  return "";
}
