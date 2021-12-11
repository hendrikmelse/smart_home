import json
import socket

CONTROLLER_IP = "192.168.1.33"
CONTROLLER_PORT = 13579

class LedGridClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def __enter__(self):
        self.sock.connect((CONTROLLER_IP, CONTROLLER_PORT))
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.sock.close()
        return
    
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
    
    def fill_rectangle(self, x1, y1, x2, y2, r, g, b, show=True):
        self._send({
            "command": "fill_rectangle",
            "position": [x1, y1, x2, y2],
            "color": [r, g, b],
            "show": show,
        })
    
    def set_custom(self, data, show=True):
        # Data expected format is [[x1, y1, r, g, b], [x2, y2, r, g, b], ...]
        self._send({
            "command": "set_custom",
            "data": data,
        })
    
    def _send(self, packet):
        self.sock.sendall(f"{json.dumps(packet)}\n".encode())