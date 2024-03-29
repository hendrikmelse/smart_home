import asyncio
import socket
import queue
import json
import time
import logging as log
import subprocess
import yaml
import requests
from requests.exceptions import ConnectionError


MAX_MSG_SIZE = 1023

DEFAULT_LOCK_TIMEOUT = 60

AVAILABLE_LED_COMMANDS = (
    "clear",
    "fill",
    "fill_rectangle",
    "set_custom",
    "show",
    "brightness",
)


class GridManager:

    def __init__(self):
        self.locking_client = None
        self.lock_timeout = time.time()
        self.packet_queue = queue.SimpleQueue()

        while True:
            try:
                manager_info = yaml.safe_load(requests.get("https://raw.githubusercontent.com/hendrikmelse/smart_home/master/config/managers.yaml").text)["led_grid"]
                device_info = yaml.safe_load(requests.get("https://raw.githubusercontent.com/hendrikmelse/smart_home/master/config/devices.yaml").text)["led_grid"]
                break
            except ConnectionError:
                time.sleep(5)
        
        self.manager_port = manager_info["port"]
        self.device_ip = device_info["ip_address"]
        self.device_port = device_info["port"]

    def run(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.manage_device())
        loop.create_task(self.run_server())
        loop.run_forever()

    async def run_server(self):
        """Listen for connecting clients and spawn a coroutine for each one"""

        log.info("Starting server...")

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server.bind(('', self.manager_port))
        except OSError:
            log.info("Port already in use, trying again in 120 seconds")
            await asyncio.sleep(120)
            server.bind(('', self.manager_port))
        log.info(f"Listening at port {self.manager_port} on all available interfaces")
        log.info(f"IP address is {subprocess.run(['hostname', '-I'], capture_output=True).stdout.decode().strip()}")
        server.listen(8)
        server.setblocking(False)

        loop = asyncio.get_event_loop()

        while True:
            client, _ = await loop.sock_accept(server)
            log.info(f"Connected by {client.getpeername()}")
            loop.create_task(self.handle_client(client))


    async def handle_client(self, client: socket.socket):
        """Listen for, process, and queue up packets until the client disconnects"""
        while True:
            command = await self.get_command(client)
            log.debug(f"Got command: {command}")

            # Check for disconnect
            if command == None:
                # Deactivate the lock, if held by the disconnecting client
                if client is self.locking_client:
                    self.locking_client = None
                break

            # Check if a lock has expired
            if self.locking_client is not None and time.time() > self.lock_timeout:
                log.info(f"Lock from {self.locking_client.getpeername()} has been released")
                self.locking_client = None

            # If another client currently holds the lock, drop the packet
            if self.locking_client not in (None, client):
                continue

            # If the command is an LED command, add it to the queue
            if command.get("command") in AVAILABLE_LED_COMMANDS:
                self.packet_queue.put(self.convert_to_bytes(command))

            # If the command is a lock request, set the lock (already checked for existing locks earlier)
            elif command.get("command") == "lock":
                self.locking_client = client
                timeout = command.get("timeout", DEFAULT_LOCK_TIMEOUT)
                log.info(f"Control has been locked by {client.getpeername()} for {timeout} seconds")
                self.lock_timeout = time.time() + timeout


        log.info(f"Connection closed to: {client.getpeername()}")
        client.close()

    @staticmethod
    async def get_command(client: socket.socket) -> dict:
        """Get a single object from the client (strean is ndjson)"""
        loop = asyncio.get_event_loop()

        msg = ""
        while True:
            char = (await loop.sock_recv(client, 1)).decode()
            if char == "\n" or char == "":
                break
            msg += char
        
        if msg == "":
            return None
        else:
            return json.loads(msg)

    @staticmethod
    def convert_to_bytes(cmd: dict) -> bytearray:
        """Convert a command into a bytearray that the device will understand"""

        command = cmd.get("command", None)
        show = cmd.get("show", True)
        packet = None

        if command == "clear":
            packet = [0x00 if show else 0x10]
        if command == "fill":
            r, g, b = cmd.get("color", (0, 0, 0))
            packet = [0x01 if show else 0x11, r, g, b]
        if command == "fill_rectangle":
            x1, y1, x2, y2 = cmd.get("position", (0, 0, 0, 0))
            r, g, b = cmd.get("color", (0, 0, 0))
            packet = [0x02 if show else 0x12, x1, y1, x2, y2, r, g, b]
        if command == "set_custom":
            packet = [0x03 if show else 0x13]
            data = cmd.get("data", ())
            packet.append(len(data))
            for point in data:
                packet.extend(point)
        if command == "show":
            packet = [0x0F]
        if command == "brightness":
            brightness = cmd.get("brightness", 255)
            packet = [0x80, brightness]
        
        if packet is not None:
            log.debug(f"Assembled packet: {packet}")
            return bytearray(packet)


    async def manage_device(self):
        """Manage the connection to the device itself and send it commands from the packet queue"""

        last_ping = time.time()

        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.connect((self.device_ip, self.device_port))
                except OSError:
                    log.info("Failed to connect to device, retrying in 30 seconds")
                    asyncio.sleep(30)
                    continue
                log.info("Connected to device")
                s.settimeout(1)
                while True:
                    while not self.packet_queue.empty():
                        packet = self.packet_queue.get()
                        log.debug(f"Sending packet: {packet}")
                        s.sendall(packet)

                    if time.time() - last_ping > 5:
                        s.sendall(bytearray([0xff]))
                        try:
                            s.recv(1)
                            log.debug("Successfully pinged device!")
                        except socket.timeout:
                            break
                        last_ping = int(time.time())
                        
                    await asyncio.sleep(0)  # Surrender control to any waiting client connections

            log.info("Disconnected from device")


def main():

    log.basicConfig(
        filename="/var/log/smart_home/led_grid_manager.log",
        format="%(asctime)s %(levelname)s: %(message)s",
        level=log.INFO,
    )

    manager = GridManager()
    manager.run()


if __name__ == "__main__":
    main()
