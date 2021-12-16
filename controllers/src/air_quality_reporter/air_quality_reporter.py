import time
import json
import requests
import os

from led_strip.led_strip_client import LedStripClient

def main():
    # *.api-key is .gitignored
    with open(os.path.join(os.path.dirname(__file__), "airnow.api-key")) as f:
        api_key = f.read()
    
    while True:
        with LedStripClient() as leds:

            category_colors = [
                (0, 0, 0), # Category 0 isn't a thing, here to make this 1-indexed
                (40, 160, 0),
                (255, 120, 0),
                (255, 60, 0),
                (255, 0, 0),
                (140, 30, 80),
                (120, 0, 30)
            ]

            leds.priority = 1
            leds.command_timeout = 360

            data = json.loads(
                requests.get(
                    url="https://www.airnowapi.org/aq/observation/zipCode/current/", params= {
                        "format": "application/json",
                        "zipCode": "90250",
                        "distance": "25",
                        "API_KEY": api_key,
                    }
                ).text
            )[0]

            AQI = data["AQI"]
            color = category_colors[data["Category"]["Number"]]
            
            print(f"AQI: {AQI}, setting color to {color}")
            leds.fill(*color)

            time.sleep(300)


if __name__ == "__main__":
    main()