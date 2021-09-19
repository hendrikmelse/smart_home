# led_strip_manager

This client registers itself to the server as `led_strip_manager`. It connects the the server and listens for commands. When it receives a command, it sends the appropriate signal to the led strip device.

## Receiving Payloads
Payloads to the LED strip manager should be dictionaries defining the following keys:
- `command` (string): required
- Various other keys may be defined, depending on the command sent.

If the command is an LED Command (see below), then the following keys may also be defined
- `priority` (int): optional, default 0
- `timeout` (int): optional, default 60 [seconds]
- Various other keys may be defined, depending on the command sent.

## Commands

### LED Commands
LED commands are executed according to their priority/timeout. Allowed commands are:
- `clear`: Turns off the led_strip.
- `fill`: Fill the strip with a solid color. Must define `color` as [r, g, b] to set the color, where r, g, b are integers from 0 to 255.
- `fill_section`: Fill a section of the strip with a solid color. Must define `color` as [r, g, b], and `start` and `end` as integers to define the start and end indicies of the filled section.
- `set_led`: Set a single led to a particular color. Must define `color` [r, g, b] and `index` as the index of the led to set.
- `set_custom`: Set the LEDs to a custom pattern. Must define `data` as a list of dictionaries, where each dictionary defines `color` as [r, g, b], and `index` as either an index or a list of indicies to set to that color. For example. to set the first 6 leds to [blue, blue, red, red, green, blue], you would set `data` to:
```
[
    {
        "color": [0, 0, 255],
        "index": [0, 1, 5]
    },
    {
        "color": [255, 0, 0],
        "index": [2, 3]
    },
    {
        "color": [0, 255, 0],
        "index": 4
    }
]
```

#### Timeout
The timeout defines how long the command will remain active on the strip before lower priority commands are allowed to be executed. If not defined, it defaults to 60 seconds. After the timeout is reached, the next-highest priority command that has not yet timed out will be executed.

#### Priority
The priority tells the controller whether to listed to the command or not. A higher number means higher priority. If a command is sent with the same priority as the currently running command, then the new command WILL be executed.

### Control Commands
Control commands are executed immediately, and do not have a priority or timeout associated. Control commands are:
- `brightness`: Set the overall brightness of the whole strip. Must define `brightness` as an integer between 0 and 255.
- `reset`: Reset the stored queue or pending commands. Useful for if the strip gets locked up with a long-timeout high-priority command.