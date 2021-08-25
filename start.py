"""
Script to spin up the server, configre the debugger,
and set up miscellaneous other things
"""

import logging

from server import Server

server = Server()
server.run()