import socket
import heapq
import time
import logging as log
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
        device_ip = "192.168.1.36",
        device_port = 12321,
    ):
        self._client = Client(
            name="led_strip_manager",
            description="A manager for the LED strip",
            interface="https://github.com/hendrikmelse/smart_home/tree/master/Clients/led_strip_manager",
        )
        
        log.basicConfig(
            filename="/var/log/smart_home/led_strip_manager.log",
            format="%(asctime)s %(levelname)s: %(message)s",
            level=log.INFO,
        )

        self._device_ip = device_ip
        self._device_port = device_port
        self._led_sock = None

        self._current_command = None
        self._command_queue = []

        self._idling = False

        self._control_commands = ("brightness", "reset", "show")

        log.info("Starting manager...")
    
    def run(self):
        """Run the manager"""
        with self._client:
            while True:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self._led_sock:
                    log.info("Connecting to device...")
                    try:
                        self._led_sock.connect((self._device_ip, self._device_port))
                    except OSError as ex:
                        log.warn(f"Error connecting to device: {ex}")
                        log.warn("Waiting for reset command...")
                        while self._client.get_incoming_payload()["payload"]["command"] != "reset": ...
                        continue

                    log.info("Connected")

                    self._run_processing_loop()
            
                log.info("Resetting connection to device...")

    def _run_processing_loop(self):
        while True:
            # Check for incoming packet
            packet = self._client.get_incoming_payload(blocking=False)
            if packet is not None:
                log.debug(f"Got packet: {packet}")

            if not packet:
                # No incoming packet
                if self._current_command is None:
                    self._idle()
                # Check current active command for timeout
                elif self._current_command.end_time < time.time():
                    log.debug("Current command timed out, switching to next in queue")
                    self._current_command = self._get_next_command()
                    log.debug(f"Got command: {self._current_command}")
                    if self._current_command is not None:
                        self._process_payload(self._current_command.payload)
            else:
                # Got a packet, check if it is a control command
                if packet["payload"]["command"] in self._control_commands:
                    if not self._process_control_command(packet["payload"]):
                        return
                    continue

                # Not a control command, load it into a command object and add it to the queue
                incoming_command = Command(
                    priority=packet["payload"].get("priority", 0),
                    end_time=time.time() + packet["payload"].get("timeout", 60),
                    payload=packet["payload"],
                )

                if self._current_command is None:
                    # No active command, process incoming command
                    self._current_command = incoming_command
                    if not self._process_payload(incoming_command.payload):
                        return

                elif incoming_command.priority >= self._current_command.priority:
                    # Incoming command has priority
                    if incoming_command.end_time < self._current_command.end_time:
                        # Only put the current command if the queue if it won't be
                        # already timed out by the time the new command finishes
                        log.debug("pushing current command to heap")
                        heapq.heappush(self._command_queue, self._current_command)
                    self._current_command = incoming_command
                    if not self._process_payload(incoming_command.payload):
                        return

    def _get_next_command(self):
        while True:
            if len(self._command_queue) == 0:
                return None
            
            next_command = heapq.heappop(self._command_queue)
            if next_command.end_time > time.time():
                return next_command

    def _process_payload(self, payload: dict):
        log.debug(f"Processing payload: {payload}")
        command = payload["command"]

        if command == "clear":
            return self._clear_strip(show=payload.get("show", True))
        elif command == "fill":
            return self._fill_strip(payload["color"], show=payload.get("show", True))
        elif command == "fill_section":
            return self._fill_strip_portion(payload["start"], payload["end"], payload["color"], show=payload.get("show", True))
        elif command == "set_led":
            return self._set_led(payload["index"], payload["color"], show=payload.get("show", True))
        elif command == "set_custom":
            for item in payload["data"]:
                if not self._set_leds(item["index"], item["color"], show=payload.get("show", True)):
                    return False
            return True

    def _process_control_command(self, payload: str):
        log.debug(f"Processing control command: {payload}")
        if payload["command"] == "brightness":
            return self._set_strip_brightness(payload["brightness"])
        elif payload["command"] == "reset":
            self._command_queue = []
            self._current_command = None
            self._clear_strip()
            return False
        elif payload["command"] == "show":
            return self._show()

    def _set_strip_brightness(self, brightness: int):
        return self._send_to_leds([0x80, brightness])

    def _show(self):
        return self._send_to_leds([0x0F])

    def _idle(self):
        if not self._idling:
            self._idling = True
            return self._send_to_leds([0x20])
    
    def _clear_strip(self, show=True):
        self._idling = False
        return self._send_to_leds([0x00 if show else 0x10])
    
    def _fill_strip(self, color, show=True):
        self._idling = False
        return self._send_to_leds([0x01 if show else 0x11, *color])
    
    def _fill_strip_portion(self, start_index, end_index, color, show=True):
        self._idling = False
        return self._send_to_leds([0x02 if show else 0x12, start_index, end_index, *color])
    
    def _set_led(self, index, color, show=True):
        self._idling = False
        return self._send_to_leds([0x03 if show else 0x13, 1, index, *color])
    
    def _set_leds(self, indicies, color, show=True):
        """Set several leds to the same color"""
        self._idling = False
        if type(indicies) is not list:
            indicies = [indicies]

        packet = [0x03 if show else 0x13, len(indicies)]
        for i in indicies:
            packet.extend([i, *color])

        return self._send_to_leds(packet)

    def _send_to_leds(self, packet):
        try:
            log.debug(f"Sending to leds: {packet}")
            # If no bytes are sent, connection is broken, return false
            self._led_sock.sendall(bytearray(packet))
        except ValueError:
            # A number bigger than 255 was given, pass silently
            pass
        except OSError:
            # Connection broken
            return False

        return True


def main():
    manager = LedStripManager()
    manager.run()


if __name__ == "__main__":
    main()