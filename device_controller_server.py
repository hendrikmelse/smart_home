# pylint: skip-file

import socket
import json
from smbus2 import SMBus, i2c_msg
import time
import atexit
import pickle
import threading
import logging


HOST = '192.168.1.133'
PORT = 42069

help_message = '''
Format {"cmd":<command>, <args>}

Available commands:

help - get help
    args
        none
    returns - this message
    example - '{"cmd":"help"}'

register - register a new i2c device on the bus
    args
        device: str - the name of the device to register
        address: int - the i2c address of the new device
    returns - 'success' or an error message
    example - '{"cmd":"register", "device":"led_strip", "address":16}'

unregister - remove a device from the bus
    args
        device: str - the name of the device to remove
    return 'success' or an error message
    example = '{"cmd":"unregister", "device":"led_strip"}'

list - list all available devices
    args
        none
    returns - a list of all available devices and their current priorities
    example - '{"cmd":"list"}'

send - send some bytes to a device
    args
        device: str - the name of the device
        priority: str - the priority of the command
        timeout: num - the number of seconds until control becomes available to lower priority commands
        payload: list - the bytes to send, max length 32
    returns - 'success' or an error message
    example - '{"cmd":"send", "device":"led_strip", "priority":4, "payload":[3, 255, 0, 128]}
'''

class Device():
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.priority = 0
        self.timeout = 0
    
    def __str__(self):
        return f'name: {self.name}, address: {self.address}, priority: {self.priority}'

def on_exit():
    for device in devices.values():
        device.priority = 0
        device.timeout = 0
    with open('./devices.pickle', 'wb') as f:
        pickle.dump(devices, f)
    
    logging.info('Exiting')

def execute(command):
    if command['cmd'] == 'help':
        return help_message
    
    if command['cmd'] == 'register':
        devices[command['device']] = Device(command['device'], command['address'])
        return 'success'
    
    if command['cmd'] == 'unregister':
        devices.remove(command['device'])
        return 'success'
    
    if command['cmd'] == 'list':
        return str(list(map(lambda a: str(a), devices.values())))
    
    if command['cmd'] == 'send':
        if command['priority'] >= devices[command['device']].priority or time.perf_counter() > devices[command['device']].timeout:

            i2c_lock.acquire()

            try:
                bus.i2c_rdwr(i2c_msg.write(devices[command['device']].address, command['payload']))
            except Exception as ex:
                i2c_lock.release()
                logging.error(f'Failed to send i2c data: {ex}')
                return 'Unable to send i2c data'
            
            i2c_lock.release()

            devices[command['device']].priority = command['priority']
            devices[command['device']].timeout = time.perf_counter() + command['timeout']
            return 'success'
        else:
            return 'Unable to execute command due to priority'

    return f'Command "{command["cmd"]}" not recognized'

def threaded_client(conn, addr):
    while True:
        try:
            data = conn.recv(1024)
            if data is None:
                logging.info(f'Connection to {addr[0]}:{addr[1]} closed')
                conn.close()
            try:
                command = json.loads(data.decode())
            except Exception as ex:
                logging.warning(f'Failed to parse received input: {ex}')
                logging.warning(f'Received input: {data.decode()}')
                conn.sendall('An error occurred during parsing'.encode())
                continue
            
            try:
                response = execute(command)
            except Exception as ex:
                logging.warning(f'Failed to execute command: {ex}')
                conn.sendall('An error occurred during execution'.encode())
                continue
            
            conn.sendall(response.encode())
        except Exception as ex:
            logging.error(f'Something went wrong: {ex}; terminating connection to {addr[0]}:{addr[1]}')
            conn.close()
            return


logging.basicConfig(level=logging.INFO, filename='device_controller_server.log', format='%(asctime)s %(levelname)s: %(message)s')

devices = {}
i2c_lock = threading.Lock()

atexit.register(on_exit)

with open('./devices.pickle', 'rb') as f:
    devices = pickle.load(f)

with SMBus(1) as bus:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        while True:
            try:
                s.bind((HOST, PORT))
                break
            except Exception as ex:
                logging.error(f'Error while binding socket: {ex}')
                logging.error('Retrying in 10 seconds...')
                time.sleep(10)
        logging.info(f'Socket listening on {HOST}:{PORT}')
        logging.info('Waiting for connections...')
        s.listen()
        while True:
            conn, addr = s.accept()

            logging.info(f'Connected by {addr[0]}:{addr[1]}')
            new_thread = threading.Thread(target=threaded_client, args=(conn, addr))
            logging.debug(f'Created new thread: {new_thread}')
            new_thread.start()
