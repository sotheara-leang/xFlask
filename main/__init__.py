from xflask import *
from xflask.server import Server

setup_root_dir('xFlask')

server = Server(db, filters=None)
app = server.app
