import json
import socket

CONTROLLER_IP = "192.168.1.33"
CONTROLLER_PORT = 55500

class LedGridClient:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def __enter__(self):
        self.begin()
        return self
    
    def begin(self):
        # Optionally use open/close instead of the context manager syntax
        self._sock.connect((CONTROLLER_IP, CONTROLLER_PORT))

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
    
    def close(self):
        self.sock.close()
    
    def show(self):
        self._send({
            "command": "show",
        })
    
    def set_brightness(self, brightness):
        brightness = max(0, min(100, brightness))
        self._send({
            "command": "brightness",
            "brightness": int(brightness * 255 // 100),
        })
    
    def clear(self, show=True):
        self._send({
            "command": "clear",
            "show": show,
        })
    
    def fill(self, r, g, b, show=True):
        self._send({
            "command": "fill",
            "color": [r, g, b],
            "show": show,
        })
    
    def fill_rectangle(self, x1, y1, x2, y2, r, g, b, show=True):
        self._send({
            "command": "fill_rectangle",
            "position": [x1, y1, x2, y2],
            "color": [r, g, b],
            "show": show,
        })
    
    def set_led(self, x, y, r, g, b, show=True):
        self.set_custom([[x, y, r, g, b]], show)
    
    def set_custom(self, data, show=True):
        # Data expected format is [[x1, y1, r, g, b], [x2, y2, r, g, b], ...]
        self._send({
            "command": "set_custom",
            "data": data,
            "show": show,
        })
    
    def lock(self, timeout=None):
        # Lock the grid and prevent other clients from commanding
        self._send({
            "command": "lock",
            "timeout": timeout
        })

    def _send(self, packet):
        self._sock.sendall(f"{json.dumps(packet)}\n".encode())
