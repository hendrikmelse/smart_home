import socket
import heapq
import time
from generic_clients.base_client import Client

class Command():
    def __init__(self, priority, end_time, payload):
        self.priority = priority
        self.end_time = end_time
        self.payload = payload

    def __eq__(self, other):
        return self.priority == other.priority

    def __lt__(self, other):
        # The backwardsness here is to make the desired priority
        # order work with the min-heap implementation of heapq
        return self.priority > other.priority

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
        self._command_queue = []

        self._idling = False

        self._control_commands = ["brightness", "reset"]
    
    def run(self):
        """Run the manager"""
        with self._led_sock, self._client:
            self._led_sock.connect((self.controller_ip, self.controller_port))

            while True:
                # Check for incoming packet
                packet = self._client.get_incoming_payload(blocking=False)
                
                
                if not packet:
                    # No incoming packet, check current active command for timeout
                    if self._current_command is not None and self._current_command.end_time < time.time():
                        self._current_command = self._get_next_command()
                        if self._current_command is not None:
                            self._process_payload(command.payload)
                    elif self._current_command is None:
                        self._idle()
                else:
                    print(f"Got payload: {packet}")
                    # Got a packet, parse it into a command object
                    incoming_command = Command(
                        priority=packet['payload'].get('priority', 0),
                        end_time=time.time() + packet['payload'].get('timeout', 60),
                        payload=packet['payload'],
                    )

                    if self._current_command is None:
                        # No active command, process incoming command
                        self._current_command = incoming_command
                        self._process_payload(incoming_command.payload)

                    elif incoming_command.priority >= self._current_command.priority:
                        # Incoming command has priority
                        heapq.heappush(self._command_queue, self._current_command)
                        self._current_command = incoming_command
                        self._process_payload(incoming_command.payload)

    def _get_next_command(self):
        while True:
            if len(self._command_queue) == 0:
                return None
            
            next_command = heapq.heappop(self._command_queue)
            if next_command.end_time > time.time():
                return next_command

    def _process_payload(self, payload: dict):
        print(f"Processing payload: {payload}")
        command = payload["command"]
        if command in self._control_commands:
            self._process_control_command(payload)

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

    def _process_control_command(self, payload: str):
        if payload["command"] == 'brightness':
            self._set_strip_brightness(payload['brightness'])
        elif payload["command"] == 'reset':
            self._command_queue = PriorityQueue()
            self._current_command = None
            self._clear_strip

    def _set_strip_brightness(self, brightness: int):
        self._send_to_leds([0x80, brightness])

    def _idle(self):
        if not self._idling:
            self._idling = True
            self._send_to_leds([0x20])
    
    def _clear_strip(self, show=True):
        self._idling = False
        self._send_to_leds([0x00 if show else 0x10])
    
    def _fill_strip(self, color, show=True):
        self._idling = False
        self._send_to_leds([0x01 if show else 0x11, *color])
    
    def _fill_strip_portion(self, start_index, end_index, color, show=True):
        self._idling = False
        self._send_to_leds([0x02 if show else 0x12, start_index, end_index, *color])
    
    def _set_led(self, index, color, show=True):
        self._idling = False
        self._send_to_leds([0x03 if show else 0x13, 1, index, *color])
    
    def _set_leds(self, indicies, color, show=True):
        """Set several leds to the same color"""
        self._idling = False
        if type(indicies) is not list:
            indicies = [indicies]

        packet = [0x03 if show else 0x13, len(indicies)]
        for i in indicies:
            packet.extend([i, *color])

        self._send_to_leds(packet)

    def _send_to_leds(self, packet):
        try:
            self._led_sock.sendall(bytearray(packet))
        except ValueError:
            # A number bigger than a byte was given, pass silently
            pass


def main():
    manager = LedStripManager()
    manager.run()


if __name__ == "__main__":
    main()