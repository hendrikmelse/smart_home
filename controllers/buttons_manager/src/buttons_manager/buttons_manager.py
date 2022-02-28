import socket
from led_strip_client import LedStripClient
import random
import colorsys

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("192.168.1.7", 12321))

        with LedStripClient() as strip:

            while True:
                button, action = s.recv(2)
                
                if (button, action) == (1, 2):
                    color = [int(x * 255) for x in colorsys.hls_to_rgb(random.random(), 0.5, 1)]
                    strip.fill(*color)
                elif (button, action) == (2, 2):
                    strip.idle()


if __name__ == "__main__":
    main()