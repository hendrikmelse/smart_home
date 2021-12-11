import socket
import json
from io import BlockingIOError


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
        self.connect()
        self.register(force=True)
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.unregister()
        self.disconnect()

    def connect(self) -> bool:
        """Open the connection to the server"""
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self.server_addr, self.server_port))
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
    
    def get_devices(self) -> list:
        """Get a list of registered devices"""
        packet = {
            'target': 'server',
            'payload': {'command': 'get_devices'},
        }

        self._send_packet(packet)
        return self._get_server_response().get('response')
    
    def get_device_info(self, device_name: str) -> dict:
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
    
    def get_incoming_packet(self, blocking: bool = True) -> dict:
        """Get an available payload"""
        if self._incoming_payloads:
            return self._incoming_payloads.pop(0)
        
        packet = self._get_packet(blocking)

        if packet is None or self._is_payload(packet):
            return packet
        

    def _send_packet(self, packet: dict) -> bool:
        """Send a packet to the server"""
        if not self._connected:
            return False
        
        self._sock.sendall(json.dumps(packet).encode())
    
    def _get_server_response(self) -> dict:
        """Wait for a response from the server"""
        while True:
            packet = self._get_packet()

            if self._is_payload(packet):
                self._incoming_payloads.append(packet)
                continue

            return packet
    
    def _get_packet(self, blocking: bool = True) -> dict:
        data = []
        braces = 0

        while True:
            if blocking:
                data.append(self._sock.recv(1).decode())
            else:
                try:
                    data.append(self._sock.recv(1, socket.MSG_DONTWAIT).decode())
                except BlockingIOError:
                    return None
            
            if data[-1] == '{':
                braces += 1
            elif data[-1] == '}':
                braces -= 1

            if braces == 0:
                break
        
        return json.loads(''.join(data))

    @staticmethod
    def _is_payload(packet: dict):
        """Check if a packet is a payload"""
        return 'sender' in packet.keys() and 'payload' in packet.keys()