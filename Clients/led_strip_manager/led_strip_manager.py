import socket
print(__name__)
from ..client import Client

class LedStripManager():
    def __init__(self):
        self._client = Client(
            name="led_strip_manager",
            description="A manager for the LED strip",
            interface="https://github.com/hendrikmelse/smart_home/tree/master/Clients/led_strip_manager",
        )
        
        self._led_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def run(self):
        """Run the manager"""
        with self._led_sock, self._client:    

            while True:
                packet = self._client.get_incoming_payload(blocking=True)
                payload = packet.get('payload')
                self._process_payload(payload)

    def _process_payload(self, payload: dict):
        print(payload)

def main():
    manager = LedStripManager()
    manager.run()

if __name__ == "__main__":
    main()