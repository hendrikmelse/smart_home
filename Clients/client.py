import socket
import json

class Client():
    """A generic client for interacting with the server"""

    def __init__(
        self,
        name: str,
        version: str = None,
        description: str = None,
        interface: str = None,
        server_addr: str = '192.168.1.33',
        server_port: int = 42069,
    ):
        self.name = name
        self.version = version
        self.description = description
        self.interface = interface
        
        self.server_addr = server_addr
        self.server_port = server_port

        self._sock=None
        self._connected = False

        self._incoming_payloads = []
    
    def __enter__(self):
        ...
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        ...

    def connect(self) -> bool:
        """Open the connection to the server"""
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self.server_ip, self.server_addr))
        self._connected = True
    
    def disconnect(self) -> bool:
        """Close the connection to the server"""
        if self._connected:
            self._sock.close()
            self._connected = False

    def register(self, force: bool = False) -> bool:
        """Register this device"""
        packet = {
            'target': 'server',
            'payload': {
                'command': 'register',
                'device_name': self.name,
                'description': self.description,
                'version': self.version,
                'interface': self.interface,
                'force': force,
            }
        }

        self._send_packet(packet)
        return self._get_server_response().get('success')
    
    def unregister(self) -> bool:
        """Unregister this device"""
        packet = {
            'target': 'server',
            'payload': {'command': 'unregister'},
        }

        self._send_packet(packet)
        return self._get_server_response().get('success')
    
    def get_devices(self) -> list[str]:
        """Get a list of registered devices"""
        packet = {
            'target': 'server',
            'payload': {'command': 'get_devices'},
        }

        self._send_packet(packet)
        return self._get_server_response().get('response')
    
    def get_device_info(self, device_name: str) -> dict[str, str]:
        """Get info about the specified device"""
        packet = {
            'target': 'server',
            'payload': {
                'command': 'get_device_info',
                'device_name': device_name,
            }
        }

        self._send_packet(packet)
        return self._get_server_response().get('response')
    
    def send_payload(self, target: str, payload: object) -> bool:
        """Send a payload to the specified target"""
        packet = {
            'target': target,
            'payload': payload,
        }

        self._send_packet(packet)
        return self._get_server_response().get('success')
    
    def get_incoming_payload(self, block: bool = False) -> object:
        """Get an available payload"""
        if self._incoming_payloads:
            return self._incoming_payloads.pop(0)

    def _send_packet(self, packet: dict) -> bool:
        """Send a packet to the server"""
        if not self._connected:
            return False
        
        self._sock.send(json.dumps(packet).encode())
    
    def _get_server_response(self) -> dict:
        """Wait for a response from the server"""
        while True:
            packet = json.loads(self._sock.recv(1024))

            if self._is_payload(packet):
                self._incoming_payloads.append(packet)
                continue

            return packet
    
    @staticmethod
    def _is_payload(packet: dict):
        """Check if a packet is a payload"""
        return 'sender' in packet.keys() and 'payload' in packet.keys()