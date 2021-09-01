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

        while True:
            print()
            action = menu(title="Choose an action", options=[
                'List registered devices',
                'Register self as "server_manager"',
                'Unregister self',
                'Get info about a device',
                'Quit',
            ])
            print()
            if action == 0:  # List devices
                devices = get_devices(sock)
                if len(devices) == 0:
                    print('No registered devices')
                else:
                    print('Registered devices:')
                    for device in get_devices(sock):
                        print(device)
            elif action == 1:  # Register self
                sock.sendall(format_server_message(
                    command='register',
                    device_name='server_manager',
                    description='A tool to interact with the server manually',
                ))
                response = json.loads(sock.recv(1024).decode())
                if response['success']:
                    print('Success')
                else:
                    print('Something went wrong')
            elif action == 2:  # Unregister a device
                sock.sendall(format_server_message(command='unregister'))
                response = json.loads(sock.recv(1024).decode())
                if response['success']:
                    print('Success')
                else:
                    print('Something went wrong')
            elif action == 3:  # Get info about a device
                devices = get_devices(sock)
                if len(devices) == 0:
                    print('No registered devices')
                else:
                    device = menu(
                        title='Choose a device to get info about',
                        options=devices,
                    )
                    print()
                    success, info = get_device_info(sock, devices[device])
                    if success:
                        for k, v in info.items():
                            print(f'{k}: {v}')
                    else:
                        print('Something went wrong')
                    
            elif action == 4: # Quit
                print('Goodbye')
                return
                

def menu(title=None, options=None):
    """Display a simple console menu. Return the index of the option"""

    if title is not None:
        print(title)

    if options is None:
        print('No options to choose from')
        return None
    
    for i in range(len(options)):
        print(f'{i + 1:4} - {options[i]}')

    choice = 0
    while choice < 1 or choice > len(options):
        print(f'Choose an option ({1}-{len(options)}): ', end=None)
        choice = int(input())

    return choice - 1

def get_devices(sock):
    """Query the server for a list of registered devices"""
    sock.sendall(format_server_message('get_devices'))
    response = json.loads(sock.recv(1024).decode())
    return response.get('response', None)

def get_device_info(sock, device):
    """Get information from the server about a device"""
    sock.sendall(format_server_message(
        command='get_device_info',
        device_name=device
    ))
    response = json.loads(sock.recv(1024))
    return response.get('success'), response.get('response')

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
    }).encode()

if __name__ == '__main__':
    main()
