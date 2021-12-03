# led_grid_manager

This client registers itself to the server as `led_grid_manager`. It connects to the server and listens for commands. When a command is recieved, it sends the appropriate command to the led grid device.

## Sending commands to the manager
Payloads to the grid manager must define the `command` key. Additional keys may be required depending on what the command is. There are several types of commands.

### LED Commands

LED commands directly control the state of the grid. Valid commands are:
- `clear`: Turn off the grid, no additional keys required
- `fill`: Fill the grid with the specified color. Must define the `color` key with a list of integers [r, g, b].
- `fill_rectangle`: Fill a rectangle within the grid. Must define the `position` key with a list of integers [x1, y1, x2, y2]. Must also define the `color` key with a list of integers [r, g, b].
- `set_custom`: Set LEDs within the grid individually. Must define the `data` key with a list of points, where each point is: [[x, y], [r, g, b]]
- `show`: See below

Any LED command may optionally define the `show` key, which defaults to `True` when not set. If `show` is `False`, then the grid will save the data to memory, but it will not show on the leds until a command with `show` set to `True` is sent, or the `show` command itself sent.

### Control Commands

Control commands are any commands that do not directly alter the state of the grid. They are not subject to priority rules are are always executed immediately. Control commands are:
-`brightness`: Change the brightness setting of the grid. Must also define the `brightness` key with a value 0-255.