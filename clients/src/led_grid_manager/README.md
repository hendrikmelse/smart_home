# led_grid_manager

## Sending commands to the manager
Commands to the led_grid manager are json literals. The command must define the `command` key. Some commands require additional keys, which are listed below.

### LED Commands

LED commands directly control the state of the grid. Valid commands are:
- `clear`: Turn off the grid, no additional keys required.
- `fill`: Fill the grid with the specified color. Must define the `color` key with a list of integers [r, g, b].
- `fill_rectangle`: Fill a rectangle within the grid. Must define the `position` key with a list of integers [x1, y1, x2, y2]. Must also define the `color` key with a list of integers [r, g, b].
- `set_custom`: Set LEDs within the grid individually. Must define the `data` key with a list of points to set, where each point is: [x, y, r, g, b]
- `show`: See below

Any LED command may optionally define the `show` key, which defaults to `true` when not set. If `show` is `false`, then the grid will save the data to memory, but it will not show on the leds until a command with `show` set to `True` is sent, or the `show` command itself sent.

### Control Commands

Control commands may be sent at any time, and are executed immediately.
-`brightness`: Change the brightness setting of the grid. Must also define the `brightness` key with a value 0-255.