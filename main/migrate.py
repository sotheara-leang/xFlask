from xflask.application import Application
from xflask.migrate import Migration
from xflask.sqlalchemy import db

from main import *


application = Application(db)

migration = Migration(application)

if __name__ == '__main__':
    migration.run()
