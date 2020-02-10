from xflask import db
from xflask.server import Server

server = Server(db, conf_file='test/conf/server.yml', log_file=None, filters=None)