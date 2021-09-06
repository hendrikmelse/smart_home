"""packet_validator.py"""

valid_server_commands = ['get_devices', 'get_device_info', 'register', 'unregister']

def is_valid_packet(packet) -> (bool, str):
    """
    Checks is a packet is a valid packet
    
    Args:
        packet (dict): the packet

    Returns:
        (bool, str): Whether the packet was valis or not and an error message if it is not
    """

    if 'target' not in packet.keys():
        return False, 'Packet must specify a target'
    
    if 'payload' not in packet.keys():
        return False, 'Packet must specify a payload'

    if packet['target'] != 'server':
        # The packet is not intended for the server, no checking of the payload is necessary
        return True, ''

    # The packet is intended for the server. Must check the payload
    payload = packet['payload']

    if type(payload) is not dict:
        return False, 'Payload directed at the server must be a dictionary'

    if 'command' not in payload.keys():
        return False, 'Payload directed at server must specify a command'
    
    if payload['command'] not in valid_server_commands:
        return False, f'Command "{payload["command"]}" not recognized'
    
    if payload['command'] == 'get_device_info':
        if 'device_name' not in payload.keys():
            return False, 'Payload must specify a device name'
    
    if payload['command'] == 'register':
        if 'device_name' not in payload.keys():
            return False, 'Payload must specify a device name'
    
    return True, ''