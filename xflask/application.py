import inspect
import logging
import sys

from flask import Flask
from flask.json import JSONEncoder
from flask_injector import FlaskInjector, request
from flask_sqlalchemy import SQLAlchemy
from injector import singleton as singleton
from werkzeug.utils import find_modules, import_string

from xflask.common.configuration import Configuration
from xflask.common.logger import Logger
from xflask.common.util import get_root_dir, get_file_path, get_xflask_path, import_modules
from xflask.component import Component
from xflask.web.controller import Controller
from xflask.web.error_handler import SimpleErrorHandler
from xflask.web.filter import Filter
from xflask.web.security.jwt_auth_filter import JwtAuthFilter
from xflask.web.security.jwt_auth_manager import JwtAuthManager
from xflask.web.serializer import EnumSerializer, DateTimeSerializer, ModelSerializer


class Application(object):
    DEF_CONF_FILE = 'conf/server.yml'
    DEF_LOG_FILE = 'conf/logging.yml'

    DEF_FILTERS = [JwtAuthFilter()]
    DEF_ERROR_HANDLER = SimpleErrorHandler()
    DEF_AUTH_MANAGER = JwtAuthManager()

    DEF_JSON_SERIALIZERS = [EnumSerializer(), DateTimeSerializer(), ModelSerializer()]

    def __init__(self, db, conf_file=None, filters=None, error_handler=None, auth_manager=None, json_serializers=[]):

        self.db = db
        self.conf_file = conf_file or get_file_path('main/conf/server.yml')

        self.filters = filters or self.DEF_AUTH_MANAGER
        self.error_handler = error_handler or self.DEF_ERROR_HANDLER
        self.auth_manager = auth_manager or self.DEF_AUTH_MANAGER
        self.json_serializers = json_serializers + self.DEF_JSON_SERIALIZERS

        self._pre_init()

    def run(self, host=None, port=None):
        host = host or self.conf.get('HOST')
        port = port or self.conf.get('PORT')
        self.app.run(host, port, use_reloader=False)

    def _pre_init(self):
        self._init_config()

        self._init_logging()

        self._init_app()

        self._init_db()

        # register xflask extension
        if not hasattr(self.app, 'extensions'):
            self.app.extensions = {}

        self.app.extensions['xflask'] = self

    def init(self):
        self._init_error_handler()

        self._register_models()

        self._register_components()

        self._register_controllers()

        self._register_blueprints()

        self._register_filters()

        self._init_auth_manager()

    def _init_config(self):
        self.conf = Configuration(get_xflask_path(self.DEF_CONF_FILE))
        if self.conf_file is not None:
            self.conf.merge(self.conf_file)

    def _init_logging(self):
        if self.conf.get('LOGGING') is False:
            logging.basicConfig(level=logging.DEBUG)
        else:
            self.logger = Logger(get_xflask_path(self.DEF_LOG_FILE))

            log_file = self.conf.get('LOGGING_CONF_FILE')
            if log_file is not None:
                self.logger.merge(log_file)

        self.logger = logging.getLogger(self.__class__.__name__)

    def _init_app(self):
        self.app = Flask(self.conf.get('APP_NAME'),
                         static_folder=self.conf.get('STATIC_DIR'),
                         template_folder=self.conf.get('TEMPLATE_DIR'),
                         root_path=get_root_dir())

        # config
        self.app.config.from_mapping(self.conf.cfg)

        # json encoder
        json_serializers = self.json_serializers

        class _JsonEncoder(JSONEncoder):

            def default(self, obj):
                for serializer in json_serializers:
                    if serializer.check(obj):
                        return serializer.serialize(obj)

                return super().default(obj)

        self.app.json_encoder = _JsonEncoder

    def _init_db(self):
        if self.conf.exist('SQLALCHEMY_DATABASE_URI'):
            self.db.init_app(self.app)

    def _init_auth_manager(self):
        if self.auth_manager is None:
            return

        self.auth_manager.init(self)

    def _init_error_handler(self):
        self.error_handler.init(self)

    def _register_filters(self):
        for filter_ in self.filters:
            if isinstance(filter_, Filter):
                filter_.init(self)
                self.app.before_request(filter_.before)
                self.app.after_request(filter_.after)
            else:
                self.logger.debug('!!! Invalid filter: %s', filter_.__name__)

    def _register_blueprints(self):
        for package in self.conf.get('BLUEPRINT_PKG'):
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
                            self.logger.error('!!! Failed to register blueprint: ', e)
            except Exception as e:
                self.logger.error('!!! Failed to find blueprint module in package: %s', package, e)

    def _register_models(self):
        import_modules(get_root_dir(), self.conf.get('MODEL_PKG'))

    def get_component(self, clazz):
        return self.flask_injector.injector.get(clazz)

    def _register_components(self):

        def configure(binder):
            # config
            binder.bind(Configuration, self.conf, scope=singleton)

            # db
            if self.conf.exist('SQLALCHEMY_DATABASE_URI'):
                binder.bind(SQLAlchemy, to=self.db, scope=singleton)

            # component
            for package in self.conf.get('COMPONENT_PKG'):
                try:
                    self.logger.debug('>>> Scan modules in %s', package)

                    for pkg_name in find_modules(package):
                        try:
                            module = import_string(pkg_name)
                            class_names = [m[0] for m in inspect.getmembers(module, inspect.isclass) if
                                           m[1].__module__ == module.__name__]

                            valid_module = False
                            for class_name in class_names:
                                obj = getattr(module, class_name)

                                if issubclass(obj, Component):
                                    if obj.abstract is True:
                                        continue

                                    valid_module = True

                                    scope = singleton if obj.scope == 'singleton' else request
                                    binder.bind(obj, obj, scope)

                                    self.logger.debug('Register component: %s', class_name)
                                else:
                                    del module
                                    self.logger.debug('!!! Invalid component: %s', class_name)

                            if not valid_module:
                                del module

                        except Exception as e:
                            self.logger.exception('!!! Failed to initialize component in %s', pkg_name, e)
                            sys.exit()

                except Exception:
                    self.logger.debug('!!! No modules founded in %s', package)

        self.flask_injector = FlaskInjector(app=self.app, modules=[configure])

    def _register_controllers(self):
        for package in self.conf.get('CONTROLLER_PKG'):
            try:
                self.logger.debug('>>> Scan modules in %s', package)

                for module_ns in find_modules(package):
                    try:
                        module = import_string(module_ns)
                        class_names = [m[0] for m in inspect.getmembers(module, inspect.isclass) if
                                       m[1].__module__ == module.__name__]

                        valid_module = False
                        for class_name in class_names:
                            controller = getattr(module, class_name)

                            if issubclass(controller, Controller):
                                if controller.abstract is True:
                                    continue

                                valid_module = True

                                try:
                                    controller.register(self.app, self.flask_injector.injector)
                                except Exception:
                                    self.logger.exception('Failed to initialize controller: %s', class_name)
                                    sys.exit()

                                self.logger.debug('Register controller: %s', class_name)
                            else:
                                self.logger.debug('!!! Invalid controller: %s', class_name)

                        if not valid_module:
                            del module

                    except Exception as e:
                        self.logger.exception('!!! Failed to initialize controller in %s', module_ns, e)
                        sys.exit()

            except Exception:
                self.logger.debug('!!! No modules found in %s', package)

        # display registered routes
        self.logger.debug('>>> Registered routes:')

        routes = self.app.url_map._rules
        if routes is not None and len(routes) > 0:
            max_len = max([len(route.rule) for route in routes])
            for route in routes:
                self.logger.debug('%*s | %26s | %s', max_len, route.rule, route.methods, route.endpoint)
