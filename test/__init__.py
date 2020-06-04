from main.context import AppContextInitializer
from xflask.application import Application
from xflask.common.util import setup_env
from xflask.sqlalchemy import db
from xflask.web.filter import ApiLoggingFilter

setup_env('xFlask')

application = Application(db, conf_file='test/conf/server.yml')
application.set_filters([ApiLoggingFilter])
application.set_listeners([AppContextInitializer])
