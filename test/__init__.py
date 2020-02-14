from xflask import *
from xflask.common import setup_root_dir
from xflask.server import Server

setup_root_dir('xFlask')

server = Server(db, conf_file='test/conf/server.yml', log_file='test/conf/logging.yml')