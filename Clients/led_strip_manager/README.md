# led_strip_manager

This client registers itself to the server as `led_strip_manager`.

## Receiving Payloads
Payloads to the LED strip manager should be dictionaries defining the following keys:
- `command` (string): required
- `priority` (int): optional, default 0
- `timeout` (int): optional, default 60 [seconds]
- `data`: sometimes required, depending on command

### Commands
In order to turn on/off leds, you must send a command. Allowed commands are:
- `brightness`: Set the overall brightness of the whole strip. Must define `data` as an integer between 0 and 255.
- `clear`: Turns off the led_strip.
- `fill`: Fill the strip with a solid color. Must define `data` as[r, g, b] to set the color, where r, g, b are integers from 0 to 255.
- `fill_section`: Fill a section of the strip with a solid color. Must define `data` as [[r, g, b], start, end] to set the color and the start and end indicies.
- `set_led`: Set a single led to a particular color. Must define `data` as [[r, g, b], index] to set the color and the led.
- `set_custom`: Set the LEDs to a custom pattern. Must define `data` as a list, where each element of the list contains the color, and a list of indicies to set to that color. For example, to set the first 5 leds to [blue, blue, red, red, blue], you would define `data` as.
```
[
    [
        [0, 0, 255],
        [0, 1, 4]
    ],
    [
        [255, 0, 0],
        [2, 3]
    ]
]
```

### Timeout
The timeout defines how long the command will remain active on the strip before lower priority commands are allowed to be executed. If not defined, it defaults to 60 seconds. After the timeout is reached, the next-highest priority command that has not yet timed out will be executed.

### Priority
The priority tells the controller whether to listed to the command or not. A higher number means higher priority. If a command is sent with the same priority as the currently running command, then the new command WILL be executed.