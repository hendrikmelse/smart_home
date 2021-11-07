import socket
import json
import tenacity
import threading
from enum import Enum
import logging as log

from device import Device
from packet_validator import is_valid_packet

HOST = "192.168.1.33"
PORT = 42069

reserved_device_names = [
    "server",
    "gerald"
]

class Server():
    """The server"""

    server_interface = "https://github.com/hendrikmelse/smart_home/blob/master/server/README.md"
    
    def __init__(self):
        log.basicConfig(
            filename="/var/log/smart_home/server.log",
            format="%(asctime)s %(levelname)s: %(message)s",
            level=log.INFO,
        )

        # keys are addresses: (ip_address: str, port: int)
        # values are device names: str
        self.device_directory = {}
    
        # keys are device names: str
        # values are device objects: Device
        self.devices = {}

    def run(self):
        """Run the server."""

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.sock:
            self._bind_sock()

            log.info("Waiting for connections...")
            self.sock.listen()

            while True:
                conn, addr = self.sock.accept()
                log.info(f"Connected by {addr[0]}:{addr[1]}")

                th = threading.Thread(target=self._client_handler, args=(conn, addr))
                th.start()

                log.debug(f"Active threads: {threading.active_count()}")

    @tenacity.retry(
        reraise=True,
        stop=tenacity.stop_after_attempt(10),
        wait=tenacity.wait_fixed(10),
    )
    def _bind_sock(self):
        """
        Attempt to bind the socket. Retry 10 times at 10 second intervals.
        
        Preconditions:
            Socket must be initialized
        """
        try:
            log.info(f"Binding socket to {HOST}:{PORT}...")
            self.sock.bind((HOST, PORT))
            log.info(f"Socket bound to {HOST}:{PORT}")
        except Exception as e:
            log.warning(e)
            raise

    def _client_handler(self, conn, addr):
        """Listen for incoming packets and process them."""
        while True:
            # Get data
            try:
                data = conn.recv(1024)
            except ConnectionResetError:
                log.info(f"Connection reset by peer: {addr[0]}:{addr[1]}")
                conn.close()
                return

            if data == b"":
                log.info(f"Closing connection to {addr[0]}:{addr[1]}")
                conn.close()
                return
            
            # Turn data from bytes into string
            data = data.decode()
            log.debug(f"{addr}: Received packet: {data}")

            # Parse data
            try:
                packet = json.loads(data)
            except Exception as ex:
                log.info(f"{addr}: Failed to parse packet: {ex}")
                self._send_response(
                    conn,
                    addr,
                    success=False, 
                    error_message="Packet must be a valid json literal no longer than 1024 characters",
                )
                continue
            
            if packet.get("target").lower() == "gerald":
                log.warn("Someone knows my real name!")
                packet["target"] = "server"

            # Validate packet
            valid, error_message = is_valid_packet(packet)
            if not valid:
                log.info(f"{addr}: Invalid packet: {error_message}")
                self._send_response(
                    conn,
                    addr,
                    success=False,
                    error_message=error_message,
                )
                continue

            # Process packet
            if packet["target"].lower() == "server":
                # Packet is intended for the server
                success, kwargs = self._server_process_packet(conn, addr, packet["payload"])
            else:
                success, kwargs = self._process_packet(addr, packet["target"].lower(), packet["payload"])
            
            self._send_response(conn, addr, success, **kwargs)

    def _send_response(self, conn, addr, success, **kwargs):
        """
        Send a response back to the client
        
        Parameters:
            conn (socket): The socket object to send the response to
            addr ((str, int)): The IP address and port number of the connections address
            success (bool): Whether to send a success response or a fail response
            **kwargs (any): Any additional items to be included in the response packet
        
        Returns:
            None
        """
        
        r = {
            "success": success,
            **kwargs,
        }
        
        r = json.dumps(r, separators=(",", ":"))
        
        log.debug(f"{addr}: Sending response: {r}")
        conn.sendall(r.encode())

    def _process_packet(self, source_addr, target_name, payload):
        """
        Execute a command from a device

        Parameters:
            source_addr ((str, int)): The source IP address and port number
            target_name (str): The name of the device being targeted
            payload (any): The payload to be passed to the target device
        
        Returns:
            (bool, dict): Whether the command was processed successfully, and the dict to be included in the response
        """
        
        if target_name not in self.devices:
            return False, {"error_message": f"Device \"{target_name}\" is not a registered device"}
        
        if source_addr not in self.device_directory:
            return False, {"error_message": "Device must be registered to send packets to other devices"}

        target_device = self.devices[target_name]
        source_name = self.device_directory[source_addr]

        packet = {
            "sender": source_name,
            "payload": payload,
        }

        target_device.socket.sendall(json.dumps(packet, separators=(",", ":")).encode())

        return True, {}
        

    def _server_process_packet(self, conn, addr, payload):
        """
        Execute a command directed at the server
        
        Parameters:
            conn (socket): The socket object to send the response to
            addr ((str, int)): The IP address and port number of the connections address
            payload (dict): The command payload for the server to parse
        
        Returns:
            (bool, dict): Whether the command was processed successfully, and the dict to be included in the response
        """

        command = payload["command"]

        if command == "get_devices":
            return True, {"response": list(self.devices.keys())}
        
        elif command == "get_device_info":
            device_name = payload["device_name"]

            if device_name not in self.devices:
                return False, {"error_message": f"Device \"{device_name}\" not recognized"}
            
            device = self.devices[device_name]

            response = {
                "name": device.name,
                "description": device.description,
                "version": device.version,
                "interface": device.interface,
            }

            # Remove any elements that are not populated
            response = {k: v for k, v in response.items() if v is not None}

            return True, {"response": response}

        elif command == "register":
            device_name = payload["device_name"].lower()
            force_register = payload.get("force", False)

            if device_name in reserved_device_names:
                return False, {"error_message": f"The device name \"{device_name}\" is reserved"}

            if device_name is None:
                return False, {"error_message": "Device name cannot be None"}

            if device_name in self.devices and not force_register:
                return False, {"error_message": f"Device \"{device_name}\" already registered"}

            if addr in self.device_directory and not force_register:
                return False, {"error_message": f"This address is already registered to a different_device: {self.device_directory[addr]}"}

            # If exists, delete old device at same address
            if addr in self.device_directory:
                self.devices.pop(self.device_directory[addr])

            self.device_directory[addr] = device_name

            self.devices[device_name] = Device(
                name=device_name,
                socket=conn,
                address=addr,
                version=payload.get("version"),
                description=payload.get("description"),
                interface=payload.get("interface"),
            )

            return True, {}

        elif command == "unregister":
            if addr not in self.device_directory:
                return False, {"error_message": "Cannot unregister a device that is not registered"}
            
            self.devices.pop(self.device_directory[addr])
            self.device_directory.pop(addr)

            return True, {}


def main():
    server = Server()
    server.run()

if __name__ == "__main__":
    main()