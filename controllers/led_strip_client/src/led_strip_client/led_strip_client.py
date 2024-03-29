import json
import socket
import requests
import yaml

CONTROLLER_IP = "192.168.1.33"
CONTROLLER_PORT = 55501

class LedStripClient:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        manager_info = yaml.safe_load(requests.get("https://raw.githubusercontent.com/hendrikmelse/smart_home/master/config/managers.yaml").text)["led_strip"]
        self.manager_ip = manager_info["ip_address"]
        self.manager_port = manager_info["port"]

    def begin(self):
        self._sock.connect((CONTROLLER_IP, CONTROLLER_PORT))

    def __enter__(self):
        self.begin()
        return self

    def close(self):
        self._sock.close()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def show(self):
        self._send({
            "command": "show",
        })
    
    def set_brightness(self, brightness):
        self._send({
            "command": "brightness",
            "brightness": brightness * 255 // 100,
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
            "command": "fill_section",
            "section": [min(start, end), max(start, end)],
            "color": [r, g, b],
            "show": show,
        })
    
    def set_led(self, index, r, g, b, show=True):
        self.set_custom([[index, r, g, b]], show)
    
    def set_custom(self, data, show=True):
        # Data expected format is [[x1, r, g, b], [x2, r, g, b], ...]
        self._send({
            "command": "set_custom",
            "data": [x for x in data if 0 <= x[0] < 60],
            "show": show,
        })
    
    def idle(self):
        self._send({
            "command": "idle",
        })
    
    def _send(self, packet):
        self._sock.sendall(f"{json.dumps(packet)}\n".encode())