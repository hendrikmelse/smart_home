"""
Script to spin up the server
and set up miscellaneous other things
"""

import logging

from server.server import Server

server = Server()
server.run()