from xflask.common.util import setup_root_dir
from xflask.application import Application
from xflask.sqlalchemy import db
from xflask.web.filter.api_logging_filter import ApiLoggingFilter


setup_root_dir('xFlask')

server = Application(db, conf_file='test/conf/server.yml', filters=[ApiLoggingFilter()])
