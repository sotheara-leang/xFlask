import inspect
import logging
import os

from flask import Flask
from flask_injector import FlaskInjector, request
from flask_sqlalchemy import SQLAlchemy
from injector import singleton as singleton
from singleton_decorator import singleton as singleton_
from werkzeug.utils import find_modules, import_string

from .common.util import get
from .common.configuration import Configuration
from .common.logger import Logger
from .web.auth_manager import JWTAuthManager
from .web.filter import AuthTokenFilter
from .web.error_handler import SimpleErrorHandler


@singleton_
class Server(object):

    def __init__(self, db, conf_file=None, log_file=None,
                 bp_pkgs=None, bean_pkgs=None, filters=None, error_handler=None, auth_manager=None):

        self.db             = db
        self.conf_file      = get(conf_file, 'main/conf/server.yml')
        self.log_file       = get(log_file, 'main/conf/logging.yml')
        self.bp_pkgs        = get(bp_pkgs, ['main.controller'])
        self.bean_pkgs      = get(bean_pkgs, ['main.dao', 'main.service'])

        self.filters        = get(filters, [AuthTokenFilter()])
        self.error_handler  = get(error_handler, SimpleErrorHandler())
        self.auth_manager   = get(auth_manager, JWTAuthManager())

        self._pre_init()

    def run(self):
        self.init()

        self.app.run(self.conf.get('HOST'), self.conf.get('PORT'), use_reloader=False)

    def _pre_init(self):
        self._init_config()

        self._init_logging()

        self._init_app()

        self._init_db()

        self._init_auth_manager()

    def init(self):
        for filter_ in self.filters:
            filter_.init(self)

        if self.error_handler is not None:
            self.error_handler.init(self)

        self._register_blueprints()

        self._register_components()

    def _init_config(self):
        self.conf = Configuration(self.conf_file)
        self.conf.set('PROJ_HOME', os.getcwd())

    def _init_app(self):
        self.app = Flask(self.conf.get('APP_NAME'),
                    static_folder=self.conf.get('STATIC_DIR'),
                    template_folder=self.conf.get('TEMPLATE_DIR'),
                    root_path=self.conf.get('PROJ_HOME'))

        self.app.config.from_mapping(self.conf.cfg)

    def _init_logging(self):
        if self.log_file is None or self.conf.get('LOGGING') is False:
            logging.basicConfig(level=logging.DEBUG)
        else:
            Logger(self.log_file)

        self.logger = logging.getLogger(self.__class__.__name__)

    def _init_db(self):
        if self.conf.exist('SQLALCHEMY_DATABASE_URI'):
            self.db.init_app(self.app)

    def _init_auth_manager(self):
        if self.auth_manager is None:
            return

        self.auth_manager.init(self)

    def _register_blueprints(self):
        for package in self.bp_pkgs:
            for name in find_modules(package):
                try:
                    module = import_string(name)
                    if hasattr(module, 'Blueprint'):
                        self.app.register_blueprint(module.bp)
                except Exception as e:
                    if not isinstance(e, AttributeError):
                        self.logger.error('fail to register blueprint: ', e)

    def _register_components(self):

        def configure(binder):
            # config
            binder.bind(Configuration, self.conf, scope=singleton)

            # db
            if self.conf.exist('SQLALCHEMY_DATABASE_URI'):
                binder.bind(SQLAlchemy, to=self.db, scope=singleton)

            for package in self.bean_pkgs:
                for pkg_name in find_modules(package):
                    try:
                        module = import_string(pkg_name)

                        class_names = [m[0] for m in inspect.getmembers(module, inspect.isclass) if
                                       m[1].__module__ == module.__name__]
                        for class_name in class_names:
                            obj = getattr(module, class_name)
                            scope = singleton if obj.scope == 'singleton' else request

                            binder.bind(obj, obj, scope)

                            self.logger.debug('register component: %s', class_name)
                    except Exception as e:
                        self.logger.error('fail to register component', e)

        self.flask_injector = FlaskInjector(app=self.app, modules=[configure])
