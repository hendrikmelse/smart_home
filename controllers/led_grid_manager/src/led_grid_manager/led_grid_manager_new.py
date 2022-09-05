import logging
from typing import Tuple
from flask import Flask
from flask_restful import Resource, Api
from flask import request
from .grid_connection import GridConnection
from typing import Tuple

logging.basicConfig(
    #filename="/var/log/smart_home/led_grid_manager.log",
    format="{asctime} {name} {levelname}: {message}",
    style="{",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)
grid_connection = GridConnection()

def to_rgb(color: str) -> Tuple[int, int, int]:
    return int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)

class Grid(Resource):
    """Restful API resource for interacting with the LED grid"""

    def get(self):
        command = request.args.get("command")
        logger.info(f"Got command: {command}")
        if command == "clear":
            grid_connection.clear()
        elif command == "fill":
            r, g, b = to_rgb(request.args.get("color"))
            grid_connection.fill(r, g, b)


def main():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Grid, "/led-grid")
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()