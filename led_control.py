from rpi_ws281x import *
from PIL import Image
import datetime
import pytz
import requests
import random
import math
import time

LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 25      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Brightnesses of each color will be scaled according to these values
# Needed because blues and greens appear much brighter to the human eye,
#   so by scaling them down, we get a much more pleasent look
MAX_R = 255
MAX_G = 150
MAX_B = 180

# Control file containing mode parameter, other needed information
CONTROL_FILE = "/var/www/html/mode.html"

# Bounce mode parameters
accel = 0.02  # downward velocity change per frame
bounce = 0.85  # velocity multiplier at bounce
reshoot = 2  # height below which a reshoot will be triggered
max_velocity = math.sqrt(117*accel)
min_velocity = 0.75 * math.sqrt(117*accel)

particles = []

# Defines the particles present in Bounce mode
particle_colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255)
]

# Picture mode parameters
PICTURE_FILE = "image.txt"
PICTURE_HOLD_MS = 7
PICTURE_SPACING_MS = 30

# Sine table for mapping brightnesses to better values
SINE_TABLE = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5,
    5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 12, 13, 13, 14, 14, 15, 16, 16, 17, 17, 18,
    18, 19, 20, 20, 21, 21, 22, 23, 23, 24, 25, 25, 26, 27, 27, 28, 29, 30, 30, 31, 32, 33, 33, 34, 35, 36, 37,
    37, 38, 39, 40, 41, 42, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61,
    62, 63, 64, 65, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 79, 80, 81, 82, 83, 84, 86, 87, 88, 89, 90, 91,
    93, 94, 95, 96, 98, 99, 100, 101, 103, 104, 105, 106, 108, 109, 110, 112, 113, 114, 115, 117, 118, 119, 121,
    122, 123, 125, 126, 127, 129, 130, 132, 133, 134, 136, 137, 139, 140, 141, 143, 144, 146, 147, 148, 150, 151,
    153, 154, 156, 157, 159, 160, 161, 163, 164, 166, 167, 169, 170, 172, 173, 175, 176, 178, 179, 181, 182, 184,
    185, 187, 188, 190, 191, 193, 194, 196, 197, 199, 200, 202, 204, 205, 207, 208, 210, 211, 213, 214, 216, 217,
    219, 221, 222, 224, 225, 227, 228, 230, 231, 233, 235, 236, 238, 239, 241, 242, 244, 246, 247, 249, 250, 252, 253, 255]

# list for pixel values, write to this, then from here to the strip in one step, makes things more efficient
pixels = [[0, 0, 0]] * LED_COUNT

def set_pixel(pixels, i, r, g ,b):
    pixels[i] = [math.ceil(SINE_TABLE[min(r, 255)] * MAX_R / 255),
                 math.ceil(SINE_TABLE[min(g, 255)] * MAX_G / 255),
                 math.ceil(SINE_TABLE[min(b, 255)] * MAX_B / 255)]


def add_color(pixels, i, r, g, b):
    pixels[i][0] = min(255, pixels[i][0] + r)
    pixels[i][1] = min(255, pixels[i][1] + g)
    pixels[i][2] = min(255, pixels[i][2] + b)


def fill(pixels, r, g, b):
    for i in range(LED_COUNT):
        pixels[i] = [r, g, b]


def fill_num(pixels, i, r, g, b):
    for n in range(i):
        add_color(pixels, n, r, g, b)


def display_custom(pixels, data):
    for i in range(0, 360, 6):
        pixels[int(i/6)] = [int("0" + data[i:i+2], 16), int("0" + data[i+2:i+4], 16), int("0" + data[i+4:i+6], 16)]


def show_pixels(strip, pixels):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(round(SINE_TABLE[pixels[i][0]] * MAX_R / 255),
                                     round(SINE_TABLE[pixels[i][1]] * MAX_G / 255),
                                     round(SINE_TABLE[pixels[i][2]] * MAX_B / 255)))
    strip.show()


strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()


while True:
    time_start = time.perf_counter()

    f = open(CONTROL_FILE, "r")
    mode = f.readline().strip()

    # Turn the led strip off
    if (mode == "Off"):
        fill(pixels, 0, 0, 0)
    
    # Testing mode, for testing various things
    elif (mode == "Test"):
        fill(pixels, 0, 0, 0)
        for i in range(255):
            strip.setPixelColor(0, Color(i, 0, 0))
            strip.setPixelColor(1, Color(0, i, 0))
            strip.setPixelColor(2, Color(0, 0, i))

            strip.setPixelColor(20, Color(SINE_TABLE[i], 0, 0))
            strip.setPixelColor(21, Color(0, SINE_TABLE[i], 0))
            strip.setPixelColor(22, Color(0, 0, SINE_TABLE[i]))
            strip.show()
            print(i)
            time.sleep(0.05)
        add_color(strip, 2, 0, 50, 0)

    # Clock mode, Blue shows hour, green shows minute, red shows second
    elif (mode == "Clock"):
        current_time = datetime.datetime.now(pytz.timezone("America/Los_Angeles"))
        fill(pixels, 0, 0, 0)
        for i in range(5*(current_time.hour%12), 5*(current_time.hour%12)+5):
            set_pixel(pixels, 59 - i, 0, 0, 255)
        add_color(pixels, 59-current_time.minute, 0, 255, 0)
        add_color(pixels, 59-current_time.second, 255, 0, 0)

    # Show bouncing particles
    elif (mode == "Bounce"):
        fill(pixels, 0, 0, 0)
        if len(particle_colors) > 0:
            color = particle_colors.pop()
            particles.append([0.0, min_velocity + (max_velocity-min_velocity)*random.random(), color])
        for p in particles:
            p[0] = p[0] + p[1]  # update position
            if p[0] < 0:  # if particle has dropped below zero
                p[1] = -1 * bounce * p[1]  # apply bounch physics
                p[0] = 0
            if p[1] < 0 and p[1] > -accel and p[0] < reshoot: # if at the maximum height and lower than the reshoot threshold
                particle_colors.append(p[2])  # add the color back to the colors list
                particles.remove(p)  # and remove the particle
                continue
            p[1] = p[1] - accel
            set_pixel(pixels, int(p[0]), p[2][0], p[2][1], p[2][2])
            # fill_num(pixels, int(p[0]), p[2][0], p[2][1], p[2][2])

    # Display a solid color with the specified RGB value
    elif (mode == "Solid"):
        r = int("0" + f.readline().strip())
        g = int("0" + f.readline().strip())
        b = int("0" + f.readline().strip())
        fill(pixels, r, g, b)

    # Display a custom static pattern on the leds. Formatted as
    # rrggbbrrggbbrrggbbrrggbb.......rrggbb as a big long hex number
    elif (mode == "Custom"):
        data = f.readline().strip()
        display_custom(pixels, data)

    # Show a picture from a text file, see constants defined above
    elif (mode == "Picture"):
        print("ready")
        input()
        with open(PICTURE_FILE, "r") as image:
            for line in image:
                display_custom(pixels, line.strip())
                show_pixels(strip, pixels)
                time.sleep(PICTURE_HOLD_MS / 1000)
                fill(pixels, 0, 0, 0)
                show_pixels(strip, pixels)
                time.sleep(PICTURE_SPACING_MS / 1000)
    
    # Display a timer according to the commands given
    elif (mode == "Timer"):
        command = f.readline().strip()
        time = f.readline().strip()
        if (command == Start):
            pass

    f.close()
    show_pixels(strip, pixels)
    time.sleep(max(0, 0.005 - (time.perf_counter() - time_start)))
