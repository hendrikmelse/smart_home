# Using the client

## Installation
Clone this repository, and run `pip install <smart_home_directory>/controllers`
Use the `-e` option for an editable installation

## Usage Example
```python
from led_grid import LedGridClient

with LedGridClient() as grid:
    grid.clear()
    grid.set_brightness(10)  # Set the brightness to 10%
    grid.fill(255, 0, 255, show=False)  # Fill magenta, but dont blit to the grid yet
    grid.fill_rectangle(6, 6, 9, 9, 0, 255, 0)  # Fill the center 4x4 square green
```

## Available methods:

```python
# Blit whatever LED commands have been buffered to the grid
grid.show()
```

```python
# Set the brightness of leds, 0-100
grid.set_brightness(brightness)
```

```python
# Clear the grid, default show immediately
grid.clear(show=True)
```

```python
# Fill the entire grid, default show immediately
grid.fill(r, g, b, show=True)
```

```python
# Fill a rectangular portion of the grid, default show immediately
grid.fill_rectangle(x1, y1, x2, y2, r, g, b, show=True)
```

```python
# Set a single led, default show immediately
grid.set_led(x, y, r, g, b, show=True)
```

```python
# Command a custom set of LEDs, default show immediately
# Data expected format is [[x1, y1, r, g, b], [x2, y2, r, g, b], ...]
grid.set_custom(data, show=True)
```

```python
# Lock the grid to prevent other clients from commanding it
# Not specifying a timeout will result in using the manager-specified default
grid.lock(timeout=None)
```

As an alternative to using the grid with a contect manager, you use begin/close.
This is useful when using the interactive interpreter or a jypyter notebook.

```python
from led_grid import LedGridClient

grid = LedGridClient()
grid.begin()

# Do stuff

grid.close()
```