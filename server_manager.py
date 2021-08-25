import argparse
import socket
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, default='192.168.1.33',
        help='The ip address of the server to connect to')
    parser.add_argument('--port', type=int, default='42069',
        help='The port to connect to')

    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((args.ip, args.port))


def get_devices(sock):
    response = sock.send(format_server_message('get_devices').encode())
    return response.get('response', None)

def format_server_message(command, **kwargs):
    """
    Format a message into a json literal that the server is expecting.
    
    Put the command any any keywords into payload of the message.
    """

    return json.dumps({
        'target': 'server',
        'payload': {
            'command': command,
            **kwargs,
        },
    })

if __name__ == '__main__':
    main()