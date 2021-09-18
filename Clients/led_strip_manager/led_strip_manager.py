import socket
from queue import PriorityQueue
import time
from ..client import Client

class Command():
    def __init__(self, priority, end_time, payload):
        self.priority = priority
        self.end_time = end_time
        self.payload = payload

class LedStripManager():
    """Manager for the LED strip that can keep track of priorities and timeouts"""
    def __init__(
        self,
        controller_ip = '192.168.1.36',
        controller_port = 12321,
    ):
        self._client = Client(
            name="led_strip_manager",
            description="A manager for the LED strip",
            interface="https://github.com/hendrikmelse/smart_home/tree/master/Clients/led_strip_manager",
        )
        
        self.controller_ip = controller_ip
        self.controller_port = controller_port
        self._led_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._current_command = None
        self._command_queue = PriorityQueue()
    
    def run(self):
        """Run the manager"""
        with self._led_sock, self._client:
            self._led_sock.connect((self.controller_ip, self.controller_port))

            while True:
                packet = self._client.get_incoming_payload(blocking=False)
                
                if not packet:
                    if self._current_command is not None and self._current_command.end_time < time.time():
                        self._current_command = self._get_next_command()
                        if self._current_command is not None:
                            self._process_payload(command.payload)
                    elif self._current_command is None:
                        self._idle()
                else:
                    incoming_command = Command(
                        priority=packet['payload'].get('priority', 0),
                        end_time=time.time() + packet['payload'].get('timeout', 60),
                        payload=packet['payload'],
                    )
                    if incoming_command.priority >= self._current_command.priority:
                        self._command_queue.put((self._current_command.priority, self._current_command))
                        self._current_command = incoming_command
                        self._process_payload(incoming_command.payload)

    def _get_next_command(self):
        while True:
            if self._command_queue.Empty():
                return None
            
            next_command = self._command_queue.get()
            if next_command.end_time > time.time():
                return next_command

    def _process_payload(self, payload: dict):
        command = payload["command"]

        if command == 'clear':
            self._clear_strip()
        elif command == 'fill':
            self._fill_strip(payload["color"])
        elif command == 'fill_section':
            self._fill_strip_portion(payload['start'], payload['end'], payload['color'])
        elif command == 'set_led':
            self._set_led(payload['index'], payload['color'])
        elif command == 'set_custom':
            for item in payload['data']:
                self._set_leds(item['index'], item['color'])

    def _process_control_command(self, payload: dict):
        if command == 'brightness':
            self._set_strip_brightness(payload['brightness'])
        elif command == 'reset':
            self._command_queue = PriorityQueue()
            self._current_command = None
            self._clear_strip

    def _set_strip_brightness(self, brightness: int):
        self._send_to_leds([0x80, brightness])

    def _idle(self):
        self._send_to_leds([0x81])
    
    def _clear_strip(self, show=True):
        self._send_to_leds([0x00 if show else 0x10])
    
    def _fill_strip(self, color, show=True):
        self._send_to_leds([0x01 if show else 0x11, *color])
    
    def _fill_strip_portion(self, start_index, end_index, color, show=True):
        self._send_to_leds([0x02 if show else 0x12, start_index, end_index, *color])
    
    def _set_led(self, index, color, show=True):
        self._send_to_leds([0x03 if show else 0x13, 1, index, *color])
    
    def _set_leds(self, indicies, color, show=True):
        """Set several leds to the same color"""
        if type(indicies) is not list:
            indicies = [indicies]

        packet = [0x03 if show else 0x13, len(indicies)]
        for i in indicies:
            packet.extend([i, *color])

        self._send_to_leds(packet)

    def _send_to_leds(self, packet):
        self._led_sock.sendall(bytearray(packet))
