from main.context import AppContextInitializer
from xflask.application import Application
from xflask.common.util import setup_env
from xflask.sqlalchemy import db
from xflask.web.filter import ApiLoggingFilter
from xflask.web.security.jwt_auth_filter import JwtAuthFilter
from xflask.web.security.jwt_auth_manager import JwtAuthManager

setup_env('xFlask')

application = Application(db, conf_files=['test/conf/server.yml', 'test/conf/setting.yml'])
application.set_filters([ApiLoggingFilter, JwtAuthFilter])
application.set_listeners([AppContextInitializer])
application.set_auth_manager(JwtAuthManager)
