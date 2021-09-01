# Overview
The server provides a way for devices to communicate with each other. Typically, a device will connect to the server and register itself. It will then be able to communicate with other devices registered with the server. Any device may send a packet to any other device using its registered name.

# Packets
## All Packets
Packets must be json literals which define the following keys:
- `target`: The intended recipient of the packet.
- `payload`: The content of the packet to send to the recipient.

If the packet does not define either of these keys, then the packet will not be processed.

If the packet's target is not registeed, then the packet will not be processed.

All packets sent or received must be fewer than 1024 characters long.

## Responses
The server will respond to every packet with a json literal that includes the following keys:
- `success`: Boolean indicating whether the server was successful in parsing and excecuting the command.
Depending on what the original packet was and what the response is, the server may optionally define the following keys:
- `error_message`: A string containing any error messages, will only be defines when `success` is False.
- `response`: When necessary, will contain arbitrary data depending on what it is responding to.

## Talking to the Server
If the target is `server`, then the packet will be consumed by the server directly, the payload must be a dictionaly which defines the `command` key. Depending on what the command is, the payload my also define other keys. Valid commands are:
- `get_devices`: Get a list of all currently registered devices.
- `get_device_info`: Get information about a particular device. The payload must define the `device_name` key to specify which device. The server will respond with a dictionary containing imformation about the device.
- `register`: Register a device (see below).
- `unregister`: Unregister a device (see below).

#### Example
To get information about a device registered as 'led_strip', the client would send the following packet:

`{"target": "server", "payload": {"command": "device_info", "device_name": "led_strip"}}`

If `led_strip` is a registered device, then the server might respond with:

`{"success": True, "response": {"name": "led_strip", "version": "1.0.1", "description": "A simple commandable LED strip"}}`

### Register
A device may only register itself. When registering, the payload must be a dictionary that defines the `device_name` key, which specifies the name by which other devices connected to the server can send packets to it. Optionally (and recommended), the payload may also define any or all of the following keys:
- `description`: A short description of what the device is.
- `version`: The software version of the device.
- `interface`: The interface for the device to be communicated with. Typically, the device should instead provide a link to the location of the interface document online.
This information will be made available to other devices connected to the server when requested.

#### Example
An led strip might send the following command to register itself:

`{"target": "server", "payload": {"device_name": "led_strip", "description": "A simple commandable LED strip.", "version": "1.0.1"}}`

### Unregister
A device may only unregister itself. No other payload arguments are necessary, as the server can identify the device by its ip address.

## Talking to Other Devices

### Sending Packets to Other Devices
If the target is not `Server`, then the server will check for a registered device matching the target, and forward the payload to that device. The payload does not need to have any particular format. Clients are free to structure their communication protocols any way they wish.

#### Example
To send a command to an led strip, a client might send the following packet:

`{"target": "led_strip", "payload": {"command": "on", "color": [128, 0, 255]}}`

### Receiving Packets from Other Devices
The server will forward packets to targets as json literals that define the following keys:
- `sender`: The name of the device from which the packet is coming.
- `payload`: The content of the packet.

#### Example
A packet received by an led strip might look like:

`{"sender": "smart_switch_3", "payload": {"command": "on", "color": [128, 0, 255]}}`