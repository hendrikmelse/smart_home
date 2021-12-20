# Using the client

## Installation
Clone this repository and run `pip install <smart_home_directory>/controllers`
Use the `-e` option for an editable installation

## Usage Example
```python
from led_strip import LedStripClient

with LedStripClient() as strip:
    strip.clear()
    strip.set_brightness(10)  # Set the brightness to 10%
    strip.fill(255, 0, 255, show=False)  # Fill magenta, but dont blit to the strip yet
    strip.fill_rectangle(6, 6, 9, 9, 0, 255, 0)  # Fill the center 4x4 square green
```

## Available methods:

```python
# Blit whatever LED commands have been buffered to the strip
strip.show()
```

```python
# Set the brightness of leds, 0-100
strip.set_brightness(brightness)
```

```python
# Clear the strip, default show immediately
strip.clear(show=True)
```

```python
# Fill the entire strip, default show immediately
strip.fill(r, g, b, show=True)
```

```python
# Fill a rectangular portion of the strip, default show immediately
strip.fill_rectangle(x1, y1, x2, y2, r, g, b, show=True)
```

```python
# Set a single led, default show immediately
strip.set_led(x, y, r, g, b, show=True)
```

```python
# Command a custom set of LEDs, default show immediately
# Data expected format is [[x1, y1, r, g, b], [x2, y2, r, g, b], ...]
strip.set_custom(data, show=True)
```

As an alternative to using the strip with a contect manager, you use begin/close.
This is useful when using the interactive interpreter or a jypyter notebook.

```python
from led_strip import LedStripClient

strip = LedstripClient()
strip.begin()

# Do stuff

strip.close()
```