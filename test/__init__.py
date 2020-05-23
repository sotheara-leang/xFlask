from xflask.common.util import setup_env
from xflask.application import Application
from xflask.sqlalchemy import db
from xflask.web.rest.filter import ApiLoggingFilter


setup_env('xFlask')

application = Application(db, conf_file='test/conf/server.yml', filters=[ApiLoggingFilter()])
