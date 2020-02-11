from xflask import *
from xflask.server import Server

setup_root_dir('xFlask')

server = Server(db, conf_file='test/conf/server.yml', log_file=None, filters=None)