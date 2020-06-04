from main.context import AppContextInitializer
from xflask.application import Application
from xflask.sqlalchemy import db
from xflask.web.filter import ApiLoggingFilter

application = Application(db)
application.set_filters([ApiLoggingFilter])
application.set_listeners([AppContextInitializer])

application.init()

if __name__ == '__main__':
    application.run()
