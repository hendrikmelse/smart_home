import asyncio
import json
import logging as log
import queue
import requests
from requests.exceptions import ConnectionError
import socket
import subprocess
import time
import yaml


MAX_MSG_SIZE = 1023

AVAILABLE_LED_COMMANDS = (
    "clear",
    "fill",
    "fill_section",
    "set_custom",
    "show",
    "brightness",
    "idle",
)


class StripManager:

    def __init__(self):
        self.locking_client = None
        self.lock_timeout = time.time()
        self.packet_queue = queue.SimpleQueue()

        while True:
            try:
                manager_info = yaml.safe_load(requests.get("https://raw.githubusercontent.com/hendrikmelse/smart_home/master/config/managers.yaml").text)["led_strip"]
                device_info = yaml.safe_load(requests.get("https://raw.githubusercontent.com/hendrikmelse/smart_home/master/config/devices.yaml").text)["led_strip"]
                break
            except ConnectionError:
                time.sleep(5)

        self.manager_port = manager_info["port"]
        self.device_ip = device_info["ip_address"]
        self.device_port = device_info["port"]

    def run(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self._manage_device())
        loop.create_task(self._run_server())
        loop.run_forever()

    async def _run_server(self):
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
        log.info(f"Local IP address is {subprocess.run(['hostname', '-I'], capture_output=True).stdout.decode().strip()}")
        server.listen(8)
        server.setblocking(False)

        loop = asyncio.get_event_loop()

        while True:
            client, _ = await loop.sock_accept(server)
            log.info(f"Connected by client: {client.getpeername()}")
            loop.create_task(self._handle_client(client))


    async def _handle_client(self, client: socket.socket):
        """Listen for, process, and queue up packets until the client disconnects"""
        while True:
            command = await self._get_command(client)
            log.debug(f"Got command: {command}")

            if command == None:
                break

            if command.get("command") in AVAILABLE_LED_COMMANDS:
                self.packet_queue.put(self._convert_to_bytes(command))

        
        log.info(f"Connection closed to client: {client.getpeername()}")
        client.close()

    @staticmethod
    async def _get_command(client: socket.socket) -> dict:
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
            log.debug(f"Got raw command: {msg}")
            return json.loads(msg)

    @staticmethod
    def _convert_to_bytes(cmd: dict) -> bytearray:
        """Convert a command into a bytearray that the device will understand"""

        command = cmd.get("command", None)
        show = cmd.get("show", True)
        packet = None

        if command == "clear":
            packet = [0x00 if show else 0x10]
        if command == "fill":
            r, g, b = cmd.get("color", (0, 0, 0))
            packet = [0x01 if show else 0x11, r, g, b]
        if command == "fill_section":
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
        if command == "idle":
            packet = [0x20]
        if command == "brightness":
            brightness = cmd.get("brightness", 255)
            packet = [0x80, brightness]
        
        if packet is not None:
            log.debug(f"Assembled packet: {packet}")
            return bytearray(packet)


    async def _manage_device(self):
        """Manage the connection to the device itself"""

        last_ping = time.time()

        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                await self._connect_to_device(s, self.device_ip, self.device_port)

                log.info(f"Connected to device: {s.getpeername()}")
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
            log.info("Connection to device broken")

    @staticmethod
    async def _connect_to_device(sock, ip, port):
        failed_connection_attempts = 0
        while True:
            try:
                sock.connect((ip, port))
                return
            except OSError as e:
                if failed_connection_attempts < 3:
                    log.warning(f"Failed to connect to device at ({ip}, {port})")
                    log.warning(e)
                    log.warning("Retrying in 10 seconds")
                    failed_connection_attempts += 1
                    if failed_connection_attempts == 3:
                        log.warning("Supressing future warnings like this")
                await asyncio.sleep(10)

def main():

    log.basicConfig(
        filename="/var/log/smart_home/led_strip_manager.log",
        format="%(asctime)s %(levelname)s: %(message)s",
        level=log.INFO,
    )

    manager = StripManager()
    manager.run()


if __name__ == "__main__":
    main()