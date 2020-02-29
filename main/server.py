from xflask import *
from xflask.server import Server
from xflask.common import setup_root_dir

from xflask.web.filter.api_logging_filter import ApiLoggingFilter

setup_root_dir('xFlask')

server = Server(db, filters=[ApiLoggingFilter()])
server.init()

app = server.app

if __name__ == '__main__':
    server.run()
