import time
import berserk
from berserk.exceptions import ResponseError, ApiError
import logging as log
import os
import random
import colorsys
from requests.exceptions import ChunkedEncodingError
from led_grid_client import LedGridClient

class ChessLeds:
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), "lichess.api-key")) as api_key:
            self.token = api_key.read()

    def run(self):
        log.info("Running chess leds")

        while True:
            try:
                with LedGridClient() as self.grid:
                    self.grid.set_brightness(5)

                    log.debug("Getting chess client...")
                    client = berserk.Client(berserk.TokenSession(self.token))
                    log.info("Connected to Lichess")

                    while True:
                        log.debug("Getting game stream...")
                        tv_stream = client.board.stream_tv_game()
                        log.debug("Done!")

                        try:
                            for state in tv_stream:
                                log.debug(state)

                                # If new game, clear LEDs and the in-memory board
                                if state["t"] == "featured":
                                    self.grid.clear()
                                    board = [0] * 64
                                    colors = self.select_colors()
                                
                                # Get the new board and update the leds
                                new_board = self.parse_fen(state["d"]["fen"])
                                for idx, (new, old) in enumerate(zip(new_board, board)):
                                    if new != old:  # Only update changed squares
                                        self.fill_square(idx, colors, new)
                                
                                self.grid.show()
                                board = new_board

                        except ChunkedEncodingError:
                            # When game stream breaks, just get a new one
                            pass
            except ResponseError:
                log.info("Bad gateway... resetting connection to lichess server in 30 seconds")
                time.sleep(30)


    @staticmethod
    def select_colors():
        """
        Select two random colors on the color wheel, both fully saturated,
        50% luminousity, and at least min_sep apart in hue`
        """
        min_sep = 0.25

        hue_1 = random.random()
        hue_2 = hue_1 + min_sep + (1 - 2 * min_sep) * random.random()
        return [int(x * 255) for x in colorsys.hls_to_rgb(hue_1, 0.5, 1)], [int(x * 255) for x in colorsys.hls_to_rgb(hue_2, 0.5, 1)]

    def fill_square(self, square: int, colors, new_state):
        y = square // 8
        x = square % 8
        if new_state == 0:
            color = [0, 0, 0]
        else:
            color = colors[new_state - 1]
        self.grid.fill_rectangle(x*2, y*2, x*2+1, y*2+1, *color, show=False)

    def parse_fen(self, fen: str):
        """
        Convert fen to encode only piece color information, remove slashes, and expand empty spaces
        """
        board = []
        for c in fen:
            if c == ' ':  # space indicates the end of the board part of the fen
                break
            elif c.isupper():  # White piece
                board.append(1)
            elif c.islower():  # Black piece
                board.append(2)
            elif c.isdigit():  # Empty spaces
                board.extend([0] * int(c))
        return board


def main():
    try:
        log.basicConfig(
            filename="/var/log/smart_home/led_chess_player.log",
            format="%(asctime)s %(levelname)s: %(message)s",
            level=log.INFO,
        )

        chess_player = ChessLeds()
        while True:
            try:
                chess_player.run()
            except BrokenPipeError:
                log.warning("Encountered broken pipe error, restarting")
                time.sleep(10)  # Probably grid manager went down, give it a few seconds before trying again
            except ApiError:
                log.warning("Encountered API error, restarting")
                time.sleep(10)  # berserk messed up, give it a few seconds before trying again
    except KeyboardInterrupt:
        log.info("Exiting due to keyboard interrupt")
    except:
        log.exception("Encountered exception")

if __name__ == "__main__":
    main()
