# Clients

Clients connect to the server directly.

## List of Clients

### client

A generic client, intended to be used by other clients to handle the mechanics of talking to the server and handling responses

### led_strip_manager

The led_strip_manager listens for commands, decides what to show on the LEDs, and passes commands directly to the LED strip with it's own TCP connection.