# Generic Clients

## base_client

The base client handles the mechanics of communicating with the server. It is intended to be instantiated by specialized clients

### Usage

Preferred usage is to use in a contect manager

```python
with Client(name, version, description, interface) as client:
    ...
```

Available methods are:
- client.get_devices(): Get a list of devices
- client.get_device_info(device_name): Get a dictionary with information about a device
- client.send_payload(target, payload): Send a payload to the specified device
- client.get_incoming_payload(blocking=True): Get an incoming payload