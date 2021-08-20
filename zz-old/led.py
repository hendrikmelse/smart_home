from rpi_ws281x import *
import numpy as np

LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Table to linearize brightness to human perception
B_TABLE = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5,
    5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 12, 13, 13, 14, 14, 15, 16, 16, 17, 17, 18,
    18, 19, 20, 20, 21, 21, 22, 23, 23, 24, 25, 25, 26, 27, 27, 28, 29, 30, 30, 31, 32, 33, 33, 34, 35, 36, 37,
    37, 38, 39, 40, 41, 42, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61,
    62, 63, 64, 65, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 79, 80, 81, 82, 83, 84, 86, 87, 88, 89, 90, 91,
    93, 94, 95, 96, 98, 99, 100, 101, 103, 104, 105, 106, 108, 109, 110, 112, 113, 114, 115, 117, 118, 119, 121,
    122, 123, 125, 126, 127, 129, 130, 132, 133, 134, 136, 137, 139, 140, 141, 143, 144, 146, 147, 148, 150, 151,
    153, 154, 156, 157, 159, 160, 161, 163, 164, 166, 167, 169, 170, 172, 173, 175, 176, 178, 179, 181, 182, 184,
    185, 187, 188, 190, 191, 193, 194, 196, 197, 199, 200, 202, 204, 205, 207, 208, 210, 211, 213, 214, 216, 217,
    219, 221, 222, 224, 225, 227, 228, 230, 231, 233, 235, 236, 238, 239, 241, 242, 244, 246, 247, 249, 250, 252, 253, 255]

SCALE_R = 1.0
SCALE_G = 0.7
SCALE_B = 0.7

class LedStrip():

    def __init__(self, count):
        self._strip = Adafruit_NeoPixel(count, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self._strip.begin()
        self._count = count
        self.pixels = []
        self.brightness = 1.0
        for _ in range(count):
            self.pixels.append([0, 0, 0])
    
    def show(self):
        for i in range(self._count):
            self.pixels[i] = list(np.clip(self.pixels[i], 0, 255))
            #print(f'Pixel {i} is color {self.pixels[i]}')
            self._strip.setPixelColor(i, Color(
                B_TABLE[int(self.pixels[i][0] * self.brightness * SCALE_R)],
                B_TABLE[int(self.pixels[i][1] * self.brightness * SCALE_G)],
                B_TABLE[int(self.pixels[i][2] * self.brightness * SCALE_B)]))
        self._strip.show()

    def clear(self):
        self.fill(0, 0, 0)

    def fill(self, r, g, b):
        for i in range(self._count):
            self.pixels[i] = [r, g, b]
