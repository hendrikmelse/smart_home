import socket
import json
import tenacity
import threading
from enum import Enum
import logging

from .device import Device
from .packet_validator import is_valid_packet

HOST = '192.168.1.33'
PORT = 42069

max_sock_bind_attempts = 3

class Server():
    """The server"""

    server_interface = 'Refer to PUT GITHUB LINK HERE'
    
    def __init__(self):
        self.logger = logging.getLogger

        # {address(address): str(name)}
        self.device_directory = {}
    
        # {str(name): Device(device)}
        self.devices = {}

    def run(self):
        """ Run the server. """

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.sock:
            self._bind_sock()

            self._log('Waiting for connections...')
            self.sock.listen()

            while True:
                conn, addr = self.sock.accept()
                self._log(f'Connected by {addr[0]}:{addr[1]}')

                th = threading.Thread(target=self._client_handler, args=(conn, addr))
                th.start()

    @tenacity.retry(
        reraise=True,
        stop=tenacity.stop_after_attempt(max_sock_bind_attempts),
        wait=tenacity.wait_fixed(5),
    )
    def _bind_sock(self):
        """
        Attempt to bind the socket. 
        
        Preconditions:
            Socket must be initialized
        """
        self._log(f'Binding socket to {HOST}:{PORT}...')
        self.sock.bind((HOST, PORT))
        self._log(f'Socket bound to {HOST}:{PORT}')

    def _client_handler(self, conn, addr):
        """Listen for incoming packets and execute them."""
        while True:
            # Get data
            data = b''
            while data == b'': # For some reason, there are a lot of empty packets
                data = conn.recv(1024)

            if data is None:
                self._log(f'Closing connection to {addr[0]}:{addr[1]}')
                conn.close()
            
            # Turn data from bytes into string
            data = data.decode()
            self._log(f'Received packet: {data}')

            # Parse data
            try:
                packet = json.loads(data)
            except Exception as ex:
                self._log(f'Failed to parse packet: {ex}')
                self._send_response(conn,
                    success=False, 
                    error_message='Packet must be a valid json literal no longer than 1024 characters',
                )
                continue
            
            # Validate command
            valid, error_message = is_valid_packet(packet)
            if not valid:
                self._log(f'Invalid packet: {error}')
                self._send_response(
                    conn,
                    success=False,
                    error_message=error_message,
                )

            # Excecute command
            if packet['target'].lower() == 'server':
                success, kwargs = self._server_execute(conn, addr, packet['payload'])
            else:
                success, kwargs = self._execute(self.device_directory[addr], packet['target'], packet['payload'])
            
            self._send_response(conn, success, **kwargs)

    def _send_response(self, conn, success, **kwargs):
        """Send a response back to the client"""
        
        r = {
            'success': success,
            **kwargs,
        }
        
        r = json.dumps(r)
        
        self._log(f'Sending response: {r}')
        conn.sendall(r.encode())

    def _execute(self, source: Device, target: str, payload):
        """
        Execute a command from a device
        
        returns:
            A tuple containing the response data
        """
        self._log('Executing... lol jk not really')
        

    def _server_execute(self, conn, addr, payload):
        """Execute a command directed at the server"""

        command = payload['command']

        if command == 'get_devices':
            return True, {'response': list(self.devices.keys())}
        
        elif command == 'get_device_info':
            device_name = payload['device_name']

            if device_name not in self.devices:
                return False, {'error_message': f'Device "{device_name}" not recognized'}
            
            device = self.devices[device_name]

            response = {
                'name': device.name,
                'description': device.description,
                'version': device.version,
                'interface': device.interface,
            }

            # Remove any elements that are not populated
            response = {k: v for k, v in response.items() if v is not None}

            return True, {'response': response}

        elif command == 'register':
            device_name = payload['device_name']

            if device_name in self.devices:
                return False, {'error_message': f'Device "{device_name}" already registered'}
            
            self.device_directory[addr] = device_name

            self.devices[device_name] = Device(
                name=device_name,
                socket=conn,
                address=addr,
                version=payload.get('version'),
                description=payload.get('description'),
                interface=payload.get('interface'),
            )

            return True, {}

        elif command == 'unregister':
            if addr not in self.device_directory.keys():
                return False, {'error_message': 'Cannot unregister an already unregistered device'}
            
            self.devices.pop(self.device_directory[addr])
            sef.device_directory.pop(addr)

            return True, {}

    def _log(self, message, level=None):
        """Log a message. For now, just print to the console."""
        print(f'{level}: {message}')