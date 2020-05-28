from xflask.application import Application
from xflask.web.filter import ApiLoggingFilter
from xflask.sqlalchemy import db

from main import *


application = Application(db, filters=[ApiLoggingFilter()])
application.init()

if __name__ == '__main__':
    application.run()
