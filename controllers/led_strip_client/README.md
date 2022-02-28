# Using the client

## Installation
Clone the repository and run `pip install <smart_home_directory>/controllers/led_strip_client`
Use the `-e` option for an editable installation

## Usage Example
```python
from led_strip_client import LedStripClient

with LedStripClient() as strip:
    strip.clear()
    strip.set_brightness(10)  # Set the brightness to 10%
    strip.fill(255, 0, 255, show=False)  # Fill with magenta, but don't blit to the strip yet
    strip.fill_section(3, 10, 0, 255, 0)  # Fill leds 3-10 with green
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
strip.fill_section(start, end, r, g, b, show=True)
```

```python
# Set a single led, default show immediately
strip.set_led(index, r, g, b, show=True)
```

```python
# Command a custom set of LEDs, default show immediately
# Data expected format is [[index1, r, g, b], [index2, r, g, b], ...]
strip.set_custom(data, show=True)
```

```python
# Start the strip idling
strip.idle()
```

As an alternative to using the strip with a contect manager, you can use begin/close.
This is useful when using the interactive interpreter or a jypyter notebook.

```python
from led_strip_client import LedStripClient

strip = LedstripClient()
strip.begin()

# Do stuff

strip.close()
```
