from led_grid_client import LedGridClient

with LedGridClient() as client:
    client.fill(255, 100, 0)
    client.show()