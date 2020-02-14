from xflask import *
from xflask.server import Server
from xflask.common import setup_root_dir

setup_root_dir('xFlask')

server = Server(db)
app = server.app
