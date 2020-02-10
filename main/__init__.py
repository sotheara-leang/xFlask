from xflask import db
from xflask.server import Server

server = Server(db)
app = server.app