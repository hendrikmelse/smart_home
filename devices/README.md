# Devices
Devices are the physical hardware that's controlled in the system.

## List of Devices

### led_strip_controller
Ad arduino that controls an LED strip. This device does not connect to the server directly. Instead, it's controlled by the led_strip_manager with a dedicated TCP socket seperate from the main server.