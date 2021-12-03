from generic_clients.base_client import Client

class LedStripClient:
    def __init__(
        self,
        name="led_strip_client",
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
        
        self.priority = 0
        self.command_timeout = 60
    
    def __enter__(self):
        self._client.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._client.__exit__(exc_type, exc_value, exc_traceback)
    
    def reset(self):
        payload = {
            "command": "reset",
        }
        self._send_packet(payload, send_raw=True)
    
    def show(self):
        payload = {
            "command": "show",
        }
        self._send_packet(payload, send_raw=True)
    
    def set_brightness(self, brightness):
        payload = {
            "command": "brightness",
            "brightness": brightness
        }
        self._send_packet(payload, send_raw=True)
    
    def clear(self, show=True):
        payload = {
            "command": "clear",
            "show": show
        }
        self._send_packet(payload)
    
    def fill(self, color, show=True):
        payload = {
            "command": "fill",
            "color": color,
            "show": show,
        }
        self._send_packet(payload)
    
    def fill_section(self, start_index, end_index, color, show=True):
        payload = {
            "command": "fill_section",
            "color": color,
            "start": start_index,
            "end": end_index,
            "show": show,
        }
        self._send_packet(payload)
    
    def set_led(self, index, color, show=True):
        payload = {
            "command": "set_led",
            "color": color,
            "index": index,
            "show": show,
        }
        self._send_packet(payload)
    
    def set_leds(self, indicies, color, show=True):
        payload = {
            "command": "set_custom",
            "data": [
                {
                    "color": color,
                    "index": indicies,
                }
            ],
            "show": show,
        }
        self._send_packet(payload)
    
    def _send_packet(self, payload, send_raw=False):
        if not send_raw:
            payload["priority"] = self.priority
            payload["timeout"] = self.command_timeout
        self._client.send_payload("led_strip_manager", payload)

