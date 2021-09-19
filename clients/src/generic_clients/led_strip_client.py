from generic_clients.base_client import Client

class LedStripClient():
    def __init__(
        self,
        name,
        description=None,
        version=None,
        interface=None,
        client=None
    ):

        if client:
            # The user has passed in an existing client, use that instead of creating a new one
            self._client = client
        else:
            self._client = Client(name, description=description, version=version, interface=interface)
        
        self._priority = 0
        self._command_timeout = 0
    
    def __enter__(self):
        self._client.__enter__()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._client().__exit__()
    
    def clear(color):
        payload = {
            "command": "clear",
        }
    
    def fill(self, color):
        payload = {
            "command": "fill",
            "color": color,
        }
        self._send_packet(payload)
    
    def fill_section(self, color, start_index, end_index):
        payload = {
            "command": "fill_section",
            "color": color,
            "start": start_index,
            "end": end_index,
        }
        self._send_packet(payload)
    
    def set_led(self, color, index):
        payload = {
            "command": "set_led",
            "color": color,
            "index": index
        }
        self._send_packet(payload)
    
    def set_leds(self, color, indicies):
        payload = {
            "command": "set_custom",
            "data": [
                {
                    "color": color,
                    "index": indicies,
                }
            ]
        }
        self._send_packet(payload)
    
    def _send_packet(self, payload):
        payload["priority"] = self._priority
        payload["timeout"] = self._command_timeout
        self._client.send_payload("led_strip_manager", payload)

