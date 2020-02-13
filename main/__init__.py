from xflask import *
from xflask.server import Server
from xflask.common.util import setup_root_dir

setup_root_dir('xFlask')

server = Server(db, filters=None)
app = server.app
