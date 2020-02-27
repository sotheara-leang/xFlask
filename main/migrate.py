from xflask import db
from xflask.server import Server
from xflask.common import setup_root_dir
from xflask.migrate import Migration

setup_root_dir('xFlask')

server = Server(db, filters=None)

migration = Migration(server, ['main.model'])

if __name__ == '__main__':
    migration.run()
