from rpi_ws281x import *
import datetime
import pytz
import requests
import random
import math
import time
from led import LedStrip

# Control file containing mode parameter, other needed information
CONTROL_FILE = "/var/www/html/mode.html"

# Bounce mode parameters
accel = 0.02  # downward velocity change per frame
bounce = 0.85  # velocity multiplier at bounce
reshoot = 2  # height below which a reshoot will be triggered
max_velocity = math.sqrt(117*accel)
min_velocity = 0.75 * math.sqrt(117*accel)

# In bounce mode, this list will contain [position, velocity, (color)] for each active particle
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

def display_custom(data):
    for i in range(0, 360, 6):
        strip.pixels[int(i/6)] = [int("0" + data[i:i+2], 16), int("0" + data[i+2:i+4], 16), int("0" + data[i+4:i+6], 16)]

strip = LedStrip(60)
strip.brightness = 0.2

while True:
    time_start = time.perf_counter()

    f = open(CONTROL_FILE, "r")
    mode = f.readline().strip()
    # Turn the led strip off
    if (mode == "Off"):
        strip.clear()

    # Clock mode, Blue shows hour, green shows minute, red shows second
    elif (mode == "Clock"):
        current_time = datetime.datetime.now(pytz.timezone("America/Los_Angeles"))
        strip.clear()
        for i in range(5*(current_time.hour%12), 5*(current_time.hour%12)+5):
            strip.pixels[59 - i][2] = 255
        
        strip.pixels[59-current_time.minute][1] = 255
        strip.pixels[59-current_time.second][0] = 255

    # Show bouncing particles
    elif (mode == "Bounce"):
        strip.clear()
        if len(particle_colors) > 0:
            color = particle_colors.pop()
            particles.append([0.0, min_velocity + (max_velocity-min_velocity)*random.random(), color])
        for p in particles:
            p[0] = p[0] + p[1]  # update position
            if p[0] < 0:  # if particle has dropped below zero
                p[1] = -1 * bounce * p[1]  # apply bounce physics
                p[0] = 0
            if p[1] < 0 and p[1] > -accel and p[0] < reshoot: # if at the maximum height and lower than the re-shoot threshold
                particle_colors.append(p[2])  # add the color back to the colors list
                particles.remove(p)  # and remove the particle
                continue
            p[1] = p[1] - accel
            for i in range(3):
                strip.pixels[int(p[0])][i] += p[2][i]

    # Display a solid color with the specified RGB value
    elif (mode == "Solid"):
        r = int("0" + f.readline().strip())
        g = int("0" + f.readline().strip())
        b = int("0" + f.readline().strip())
        strip.fill(r, g, b)

    # Display a custom static pattern on the leds. Formatted as
    # rrggbbrrggbbrrggbbrrggbb.......rrggbb - a big long hex number
    elif (mode == "Custom"):
        data = f.readline().strip()
        display_custom(data)

    # Show a picture from a text file, see constants defined above
    elif (mode == "Picture"):
        print("ready")
        input()
        with open(PICTURE_FILE, "r") as image:
            for line in image:
                display_custom(line.strip())
                strip.show()
                time.sleep(PICTURE_HOLD_MS / 1000)
                strip.clear()
                strip.show()
                time.sleep(PICTURE_SPACING_MS / 1000)

    f.close()
    strip.show()
    #time.sleep(max(0, 0.005 - (time.perf_counter() - time_start)))
