import inspect
import logging

from flask import Flask
from flask_injector import FlaskInjector, request
from flask_sqlalchemy import SQLAlchemy
from injector import singleton as singleton
from singleton_decorator import singleton as singleton_
from werkzeug.utils import find_modules, import_string

from xflask.common import get_root_dir, get_file
from xflask.common.configuration import Configuration
from xflask.common.logger import Logger
from xflask.component import Component
from xflask.controller import Controller
from xflask.web.security.jwt_auth_manager import JwtAuthManager
from xflask.web.security.jwt_auth_filter import JwtAuthFilter
from xflask.web.error_handler import SimpleErrorHandler


@singleton_
class Server(object):
    DEF_CONF_FILE           = 'main/conf/server.yml'
    DEF_LOG_FILE            = 'main/conf/logging.yml'
    DEF_BLUEPRINT_PKGS      = []
    DEF_CONTROLLER_PKGS     = ['main.controller.mvc', 'main.controller.rest']
    DEF_COMPONENT_PKGS      = ['main.dao', 'main.service']
    DEF_FILTERS             = [JwtAuthFilter()]
    DEF_ERROR_HANDLER       = SimpleErrorHandler()
    DEF_AUTH_MANAGER        = JwtAuthManager()

    def __init__(self, db, conf_file=DEF_CONF_FILE, log_file=DEF_LOG_FILE,
                 component_pkgs=DEF_COMPONENT_PKGS, controller_pkgs=DEF_CONTROLLER_PKGS, blueprint_pkgs=DEF_BLUEPRINT_PKGS,
                 filters=DEF_FILTERS, error_handler=DEF_ERROR_HANDLER, auth_manager=DEF_AUTH_MANAGER):

        self.db                 = db
        self.conf_file          = conf_file
        self.log_file           = log_file
        self.component_pkgs     = component_pkgs
        self.blueprint_pkgs     = blueprint_pkgs
        self.controller_pkgs    = controller_pkgs

        self.filters            = filters or []
        self.error_handler      = error_handler
        self.auth_manager       = auth_manager

        self._pre_init()

    def run(self):
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

        self._register_components()

        self._register_controllers()

        self._register_blueprints()

    def _init_config(self):
        self.conf_file = self.conf_file or self.DEF_CONF_FILE
        self.conf = Configuration(get_file(self.conf_file))

    def _init_logging(self):
        self.log_file = self.log_file or self.DEF_LOG_FILE

        if self.log_file is None or self.conf.get('LOGGING') is False:
            logging.basicConfig(level=logging.DEBUG)
        else:
            Logger(get_file(self.log_file))

        self.logger = logging.getLogger(self.__class__.__name__)

    def _init_app(self):
        self.app = Flask(__name__,
                    static_folder=self.conf.get('STATIC_DIR'),
                    template_folder=self.conf.get('TEMPLATE_DIR'),
                    root_path=get_root_dir())

        self.app.config.from_mapping(self.conf.cfg)

        #
        if not hasattr(self.app, 'extensions'):
            self.app.extensions = {}

        self.app.extensions['xflask'] = self

    def _init_db(self):
        if self.conf.exist('SQLALCHEMY_DATABASE_URI'):
            self.db.init_app(self.app)

    def _init_auth_manager(self):
        if self.auth_manager is None:
            return

        self.auth_manager.init(self)

    def _register_blueprints(self):
        for package in self.blueprint_pkgs:
            try:
                for name in find_modules(package):
                    try:
                        module = import_string(name)
                        if hasattr(module, 'Blueprint'):
                            self.app.register_blueprint(module.bp)
                        else:
                            del module

                    except Exception as e:
                        if not isinstance(e, AttributeError):
                            self.logger.error('fail to register blueprint: ', e)
            except Exception as e:
                self.logger.error('fail to find blueprint module in package: %s', package, e)

    def _register_components(self):

        def configure(binder):
            # config
            binder.bind(Configuration, self.conf, scope=singleton)

            # db
            if self.conf.exist('SQLALCHEMY_DATABASE_URI'):
                binder.bind(SQLAlchemy, to=self.db, scope=singleton)

            # component
            for package in self.component_pkgs:
                try:
                    for pkg_name in find_modules(package):
                        try:
                            module = import_string(pkg_name)

                            valid_module = False

                            class_names = [m[0] for m in inspect.getmembers(module, inspect.isclass) if
                                           m[1].__module__ == module.__name__]
                            for class_name in class_names:
                                obj = getattr(module, class_name)

                                if issubclass(obj, Component):
                                    valid_module = True

                                    scope = singleton if obj.scope == 'singleton' else request
                                    binder.bind(obj, obj, scope)

                                    self.logger.debug('register component: %s', class_name)
                                else:
                                    del module
                                    self.logger.debug('skip component: %s', class_name)

                            if not valid_module:
                                del module

                        except Exception as e:
                            self.logger.exception('fail to register component', e)
                except Exception as e:
                    self.logger.exception('fail to find component module in package: %s', package)

        self.flask_injector = FlaskInjector(app=self.app, modules=[configure])

    def _register_controllers(self):
        for package in self.controller_pkgs:
            try:
                for pkg_name in find_modules(package):
                    try:
                        module = import_string(pkg_name)

                        valid_module = False

                        class_names = [m[0] for m in inspect.getmembers(module, inspect.isclass) if
                                       m[1].__module__ == module.__name__]
                        for class_name in class_names:
                            controller = getattr(module, class_name)

                            if issubclass(controller, Controller):
                                valid_module = True

                                controller.register(self.app, self.flask_injector.injector)

                                self.logger.debug('register controller: %s', class_name)
                            else:
                                self.logger.debug('skip controller: %s', class_name)

                        if not valid_module:
                            del module

                    except Exception as e:
                        self.logger.error('fail to register controller', e)
            except Exception as e:
                self.logger.error('fail to find controller module in package: %s', package)

        # display routes
        if self.conf.get('DEBUG') is True:
            routes = self.app.url_map._rules
            max_len = max([len(route.rule) for route in routes])
            for route in routes:
                self.logger.debug('%*s | %26s | %s', max_len, route.rule, route.methods, route.endpoint)
