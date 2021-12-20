import json
import socket

CONTROLLER_IP = "192.168.1.33"
CONTROLLER_PORT = 55501

class LedStripClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def __enter__(self):
        self.sock.connect((CONTROLLER_IP, CONTROLLER_PORT))
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.sock.close()
    
    def show(self):
        self._send({
            "command": "show",
        })
    
    def set_brightness(self, brightness):
        self._send({
            "command": "brightness",
            "brightness": brightness,
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
    
    def fill_section(self, start, end, r, g, b, show=True):
        self._send({
            "command": "fill_rectangle",
            "section": [min(start, end), max(start, end)],
            "color": [r, g, b],
            "show": show,
        })
    
    def set_custom(self, data, show=True):
        # Data expected format is [[x1, r, g, b], [x2, r, g, b], ...]
        self._send({
            "command": "set_custom",
            "data": data,
            "show": show,
        })
    
    def idle(self):
        self._send({
            "command": "idle",
        })
    
    def _send(self, packet):
        self.sock.sendall(f"{json.dumps(packet)}\n".encode())