from xflask.application import Application
from xflask.sqlalchemy import db
from xflask.web.filter import ApiLoggingFilter
from xflask.web.security.jwt_auth_manager import JwtAuthManager

from main import *

application = Application(db, conf_files=['main/conf/server.yml', 'main/conf/setting.yml'])
application.set_auth_manager(JwtAuthManager)
application.register_filter(ApiLoggingFilter)

# for run with container - gunicorn
app = application.app

application.init()

if __name__ == '__main__':
    application.run()
