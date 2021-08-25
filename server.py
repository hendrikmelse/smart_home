import socket
import json
import tenacity
import threading
from enum import Enum
import logging

HOST = '192.168.1.33'
PORT = 42069

max_sock_bind_attempts = 3

class Device():
    def __init__(self, name, socket, address, version, description, interface):
        self.name = name
        self.socket = socket
        self.address = address
        self.version = version
        self.description = description
        self.interface = interface
    
    def __repr__(self):
        return (
            f'Device(name={self.name}, '
            f'address={self.address}, '
            f'version={self.version}, '
            f'description={self.description}, '
            f'interface={self.interface})'
        )


class Server():
    """
    The server is the central hub for all devices.

    Upon connecting to the server, each client must inform the server of its
    name, version, and a short description of itself, as well as a more
    detailed description of how to communicate with it.

    Any client may, at any time, query the server for information about
    currently connected devices.

    The server will also provide information to clients when queried.
    """

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
        """Listen for incoming messages and execute them."""
        while True:
            # Get data
            data = b''
            while data == b'':
                data = conn.recv(1024)

            if data is None:
                self._log(f'Closing connection to {addr[0]}:{addr[1]}')
                conn.close()
            
            # Turn data from bytes into string
            data = data.decode()
            self._log(f'Received message: {data}')

            # Parse data
            try:
                message = json.loads(data)
            except Exception as ex:
                self._log(f'Failed to interpret with exception: {ex}')
                self._send_response(conn, False, (
                    'Failed to parse data, make sure the message is a json '
                    'literal and is fewer than 1024 characters long.'
                ))
                continue

            # Excecute command
            try:
                if message['target'].lower() == 'server':
                    succ, msg, resp = self._server_execute(conn, addr, message['payload'])
                    self._send_response(conn, succ, msg, resp)
                else:
                    self._execute(self.device_directory[addr], message['target'], message['payload'])
            except Exception as ex:
                self._log(f'Failed to excecute command with exception: {ex}')
                self._send_response(conn, False, (
                    '"Failed to parse data, make sure the message is a json '
                    'literal and is fewer than 1024 characters long."'
                ))
                continue

    def _send_response(self, conn, success, message, response=None):
        """Send a response back to the client."""
        
        r = {
            'success': success,
            'message': message,
        }

        if response is not None:
            r['response'] = response
        
        r = json.dumps(r)
        
        self._log(f'Sending response: {r}')
        conn.sendall(r.encode())

    def _execute(self, source, target, payload):
        """
        Execute a command from a device
        
        returns:
            A tuple containing the response data
        """
        self._log('Executing... lol jk not really')
        

    def _server_execute(self, conn, addr, command):
        """Execute a command directed at the server"""

        response = None

        if command['command'] == 'get_devices':
            response = list(self.devices.keys())

        elif command['command'] == 'device_info':
            if command['device'].lower() in self.devices:
                response = str(self.devices[command['device'].lower()])
            else:
                return False, "Unknown device", None

        elif command['command'] == 'device_interface':
            if command['device'].lower() in self.devices:
                response = str(self.devices[command['device'].lower()].interface)
            else:
                return False, "Unknown device", None

        elif command['command'] == 'register':
            if command['name'].lower() in self.devices:
                return False, "Device already registered", None
            elif addr in self.device_directory.keys():
                return False, "Address already registered", None
            else:
                self.devices[command['name'].lower()] = Device(
                    name=command['name'].lower(),
                    socket=conn,
                    address=addr,
                    version=command.get('version', None),
                    description=command.get('description', None),
                    interface=command.get('interface', None),
                )
                self.device_directory[addr] = command['name']

        elif command['command'] == 'unregister':
            if 'device' not in command.keys():
                # Unregister by sender IP
                if addr not in self.device_directory.keys():
                    return False, "Address not registered", None
                else:
                    self.devices.pop(self.device_directory[addr])
                    self.device_directory.pop(addr)
            else:
                # Unregister by device name
                if command['device'].lower() not in self.devices.keys():
                    return False, "Device not registered", None
                else:
                    self.device_directory.pop(self.devices[command['device'].lower()].address)
                    self.devices.pop(command['device'].lower())
        
        return True, "", response

    def _log(self, message, level=None):
        """Log a message. For now, just print to the console."""
        print(f'{level}: {message}')