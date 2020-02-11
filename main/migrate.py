from main import *
from xflask.migrate import Migration

if __name__ == '__main__':
    migration = Migration(server, ['main.model'])
    migration.run()
