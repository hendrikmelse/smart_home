import time
from datetime import datetime
from led_grid_client import LedGridClient

turn_off_time = datetime(2000, 1, 1, 22, 0, 0)
off_duration = 8 * 60 * 60

def main():
    with LedGridClient() as grid:
        while True:
            now = datetime.now()
            time.sleep((turn_off_time - now).seconds)
            grid.lock(timeout=off_duration)
            grid.clear()
            time.sleep(10)


if __name__ == "__main__":
    main()