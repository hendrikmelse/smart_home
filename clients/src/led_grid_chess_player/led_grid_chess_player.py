import berserk
import os
import random
from requests.exceptions import ChunkedEncodingError
from generic_clients.led_grid_client import LedGridClient

def main():
    with open(os.path.join(os.path.dirname(__file__), "lichess.api-key")) as api_key:
        token = api_key.read()
    
    grid = LedGridClient()
    with grid:
        grid.set_brightness(5)

        while True:
            print("Getting new client...", end="")
            client = berserk.Client(berserk.TokenSession(token))
            print("Done!")
            game = client.board.stream_tv_game()

            try:
                for state in game:
                    print(state)
                    if state["t"] == "featured":
                        grid.clear()
                        board = " " * 64
                        colors = select_colors()
                    new_board = parse_fen(state["d"]["fen"])
                    for idx, (new, old) in enumerate(zip(new_board, board)):
                        if new != old:
                            fill_square(grid, idx, colors, new)
                    
                    grid.show()
                    board = new_board
            except ChunkedEncodingError:
                pass

def select_colors():
    r = [0, 1, 2]
    random.shuffle(r)
    color1 = [0, 0, 0]
    color2 = [0, 0, 0]
    color1[r[0]] = 255
    color1[r[1]] = random.randint(0, 255)
    color2[r[1]] = random.randint(0, 255)
    color2[r[2]] = 255
    return color1, color2

def fill_square(grid: LedGridClient, square: int, colors, new_state):
    y = square // 8
    x = square % 8
    if new_state == " ":
        color = [0, 0, 0]
    else:
        color = colors[int(new_state)]
    grid.fill_rectangle(x*2, y*2, x*2+1, y*2+1, color, show=False)

def parse_fen(fen: str):
    board = ""
    for c in fen:
        if c == ' ':
            break
        elif c.isupper():
            board += '1'
        elif c.islower():
            board += '0'
        elif c.isdigit():
            board += " " * int(c)
    return board

if __name__ == "__main__":
    main()