import socket
from typing import List
import logging
import time

DEVICE_IP = "192.168.1.21"
DEVICE_PORT = 12321

class GridConnection:
    """Interface for communicating with the grid directly"""

    def __init__(self) -> None:
        self.id = time.perf_counter()
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing connection")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((DEVICE_IP, DEVICE_PORT))
        self.logger.debug(f"Connected to peer: {self.sock.getpeername()}")
    
    def __del__(self) -> None:
        self.logger.debug("Closing connection")
        self.sock.close()
    
    def _send_packet(self, packet: List) -> None:
        self.logger.info(f"sending packet ({self.id}): {packet}")
        self.sock.sendall(bytearray(packet))
        self.ping()
    
    def ping(self) -> None:
        self.sock.sendall(bytearray([0xFF]))
        self.sock.recv(1)
        self.logger.debug("Got ping response")

    def clear(self, show: bool = True) -> None:
        self._send_packet([0x00 if show else 0x10])
    
    def fill(self, r: int, g: int, b:int, show: bool = True):
        self._send_packet([0x01 if show else 0x11, r, g , b])
    
    def fill_rectangle(self, x1: int, y1: int, x2: int, y2: int, r: int, g: int, b: int, show: bool = True):
        self._send_packet([0x02 if show else 0x12, x1, y1, x2, y2, r, g, b])

    def set_custom(self, data: List[List[int]], show: bool = True):
        """Data is a list of points, where each point is [x, y, r, g, b]"""
        packet = [0x03 if show else 0x13]
        packet.append(len(data))
        for point in data:
            packet.extend(point)
        self._send_packet(packet)
    
    def show(self):
        self._send_packet([0x0F])

    def set_brightness(self, brightness: int):
        self._send_packet([0x80, brightness])
