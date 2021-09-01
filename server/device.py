"""device.py"""

class Device():
    """Represent a single device."""
    def __init__(self, name, socket, address, version, description, interface):
        self.name = name
        self.socket = socket
        self.address = address
        self.version = version
        self.description = description
        self.interface = interface
    
    def __repr__(self):
        return (
            f'Device(name={self.name}, '
            f'address={self.address}, '
            f'version={self.version}, '
            f'description={self.description}, '
            f'interface={self.interface})'
        )
