import json
import socket
import requests
import yaml

CONTROLLER_IP = "192.168.1.33"
CONTROLLER_PORT = 55500

class LedGridClient:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        manager_info = yaml.safe_load(requests.get("https://raw.githubusercontent.com/hendrikmelse/smart_home/master/config/managers.yaml").text)["led_grid"]
        self.manager_ip = manager_info["ip_address"]
        self.manager_port = manager_info["port"]
        
    def begin(self):
        """Initialize the connection to the grid manager"""
        self._sock.connect((self.manager_ip, self.manager_port))

    def __enter__(self):
        self.begin()
        return self
    
    def close(self):
        """Close the connection to the grid manager"""
        self._sock.close()
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
    
    def show(self):
        """Blit anything that's in the buffer to the grid"""
        self._send({
            "command": "show",
        })
    
    def set_brightness(self, brightness):
        """Set the grid brightness"""
        brightness = max(0, min(100, brightness))
        self._send({
            "command": "brightness",
            "brightness": int(brightness * 255 // 100),
        })
    
    def clear(self, show=True):
        """Clear the entire grid"""
        self._send({
            "command": "clear",
            "show": show,
        })
    
    def fill(self, r, g, b, show=True):
        """Fill the entire grid with the specified color"""
        self._send({
            "command": "fill",
            "color": [r, g, b],
            "show": show,
        })
    
    def fill_rectangle(self, x1, y1, x2, y2, r, g, b, show=True):
        """Fill the specified rectangle with the specififed color"""
        self._send({
            "command": "fill_rectangle",
            "position": [x1, y1, x2, y2],
            "color": [r, g, b],
            "show": show,
        })
    
    def set_led(self, x, y, r, g, b, show=True):
        self.set_custom([[x, y, r, g, b]], show)
    
    def set_custom(self, data, show=True):
        """Data expected format is [[x1, y1, r, g, b], [x2, y2, r, g, b], ...]"""
        self._send({
            "command": "set_custom",
            "data": data,
            "show": show,
        })
    
    def lock(self, timeout=None):
        """Lock the grid and prevent other clients from commanding"""
        self._send({
            "command": "lock",
            "timeout": timeout
        })
    
    def unlock(self):
        """Release the lock"""
        self._send({
            "command": "lock",
            "timeout": 0
        })

    def _send(self, packet):
        self._sock.sendall(f"{json.dumps(packet)}\n".encode())
