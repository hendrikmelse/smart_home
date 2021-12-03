from generic_clients.base_client import Client

class LedGridClient:
    def __init__(
        self,
        name="led_grid_client",
        description=None,
        version=None,
        interface=None,
        client=None
    ):

        if client:
            # The user has passed in an existing client, use that instead of creating a new one
            self._client = client
        else:
            self._client = Client(
                name,
                description=description,
                version=version,
                interface=interface
            )
        
    def __enter__(self):
        self._client.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._client.__exit__(exc_type, exc_value, exc_traceback)
    
    def reset(self):
        self._send_packet({
            "command": "reset",
        })
    
    def show(self):
        self._send_packet({
            "command": "show"
        })
    
    def set_brightness(self, brightness):
        self._send_packet({
            "command": "brightness",
            "brightness": brightness
        })
    
    def clear(self):
        self._send_packet({
            "command": "clear"
        })
    
    def fill(self, color, show=True):
        self._send_packet({
            "command": "fill",
            "color": color,
            "show": show
        })
    
    def fill_rectangle(self, x1, y1, x2, y2, color, show=True):
        self._send_packet({
            "command": "fill_rectangle",
            "position": [x1, y1, x2, y2],
            "color": color,
            "show": show
        })
    
    def set_custom(self, data, show=True):
        # Data must be in format: [[[x, y], [r, g, b]], [[x, y], [r, g, b]], ...]
        self._send_packet({
            "command": "set_custom",
            "data" : data,
            "show": show
        })
    
    def _send_packet(self, payload):
        self._client.send_payload("led_grid_manager", payload)