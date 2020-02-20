from xflask import *
from xflask.server import Server
from xflask.common import setup_root_dir

setup_root_dir('xFlask')

server = Server(db, filters=None)
server.init()

app = server.app

if __name__ == '__main__':
    server.run()
