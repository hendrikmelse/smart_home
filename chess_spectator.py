# pylint: skip-file

import socket
import berserk
import json
import random
import time
import logging
from colorsys import hls_to_rgb

with open('./host.txt') as f:
    HOST = f.read()
PORT = 42069

def stream_tv_game(client):
    """
    :param berserk.Client client: client to deal with
    :returns: iterator over game states
    """

    path = 'api/tv/feed'
    yield from client.board._r.get(path, stream=True, converter=berserk.models.GameState.convert)

def send_command(payload):
    command = {'cmd':'send', 'device':'led_grid', 'priority':1, 'timeout':0, 'payload':payload}
    s.sendall(json.dumps(command).encode())
    response = s.recv(2048)
    if response != b'success':
        logging.warning(f'Command failed, server response: {response}')

def get_new_colors():
    global color_white
    global color_black
    white_hue = random.randint(0, 360)
    black_hue = random.randint(white_hue + 90, white_hue + 270)
    color_white = list(hls_to_rgb(white_hue / 360, 0.5, 1))
    color_black = list(hls_to_rgb(black_hue / 360, 0.5, 1))
    color_white[1] *= 0.7
    color_white[2] *= 0.7
    color_black[1] *= 0.7
    color_black[2] *= 0.7
    color_white = list(map(lambda a: int(255 * a), color_white))
    color_black = list(map(lambda a: int(255 * a), color_black))

def send_fill_and_show(color):
    send_command([4] + color)
    send_command([1])

def fill_2x2(x, y, color):
    payload = [5]
    payload += [2 * x, 2 * y] + color
    payload += [2 * x, 2 * y + 1] + color
    payload += [2 * x + 1, 2 * y] + color
    payload += [2 * x + 1, 2 * y + 1] + color
    send_command(payload)

def send_board_state(fen):
    rows = fen.split('/')
    for y in range(8):
        x = 0
        for char in rows[y]:
            if char.isdigit():
                for i in range(int(char)):
                    new_board_state[x][y] = [0, 0, 0]
                    x += 1
            else:
                new_board_state[x][y] = color_white if char.isupper() else color_black
                x += 1
            
            if x >= 8:
                break
    
    for x in range(8):
        for y in range(8):
            if board_state[x][y] != new_board_state[x][y]:
                board_state[x][y] = new_board_state[x][y]
                fill_2x2(x, y, board_state[x][y])

    send_command([1])


color_background = [0, 0, 0]
color_black = [0, 0, 0]
color_white = [0, 0, 0]

logging.basicConfig(level=logging.INFO, filename='chess_spectator.log', format='%(asctime)s %(levelname)s: %(message)s')

board_state = []
new_board_state = []
for i in range(8):
    board_state.append([color_background] * 8)
    new_board_state.append([color_background] * 8)

with open('./lichess.token') as f:
    token = f.read()

session = berserk.TokenSession(token)
client = berserk.Client(session)

while True:
    logging.info("Getting game stream...")
    game = stream_tv_game(client)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            logging.info(f'Connecting to {HOST}:{PORT}...')
            s.connect((HOST, PORT))
            logging.info(f'Connected')
            while True:
                state = next(game)
                if state['t'] == 'featured':
                    send_command([4, 0, 0, 0])
                    send_command([2, 10])
                    get_new_colors()
                if state['t'] == 'fen' or state['t'] == 'featured':
                    send_board_state(state['d']['fen'])
    except Exception as ex:
        logging.error(f'Something went wrong: {ex}; reconnecting in 10 seconds...')
        s.close()
        time.sleep(10)