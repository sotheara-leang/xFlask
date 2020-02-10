from xflask import db
from xflask.server import Server

server = Server(db)

if __name__ == '__main__':
    server.run()
