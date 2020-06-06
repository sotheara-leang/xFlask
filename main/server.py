from main.context import AppContextInitializer
from xflask.application import Application
from xflask.sqlalchemy import db
from xflask.web.filter import ApiLoggingFilter

application = Application(db, conf_files=['main/conf/server.yml', 'main/conf/setting.yml'])
application.set_filters([ApiLoggingFilter])
application.register_component(AppContextInitializer)

application.init()

if __name__ == '__main__':
    application.run()
