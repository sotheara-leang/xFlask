from xflask import db
from xflask.server import Server
from xflask.migrate import Migration


server = Server(db)

migration = Migration(server, ['main.model'])

if __name__ == '__main__':
    migration.run()
