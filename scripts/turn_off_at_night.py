import time
from datetime import datetime, timedelta
from led_grid_client import LedGridClient



def is_daytime(now):
    return now.hour >= 8 and (now.hour < 22 or (now.hour == 22 and now.minute < 30))

with LedGridClient() as grid:
    while True:
        now = datetime.now()
        if is_daytime(now):
            tonight = datetime(now.year, now.month, now.day, 22, 30, 0)
            time.sleep((tonight - now).total_seconds())
            grid.lock(timeout=(9.5 * 60 * 60))
            grid.clear()
        else:
            # not daytime, wait half a day until it is
            time.sleep(12 * 60 * 60)



