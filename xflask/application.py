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
from xflask.context import ApplicationStateListener
from xflask.json import JSON_SERIALIZERS
from xflask.web.controller import Controller
from xflask.web.error_handler import BasicErrorHandler
from xflask.web.error_handler import ErrorHandler
from xflask.web.filter import Filter
from xflask.web.security.auth_manager import AuthManager
from xflask.web.security.jwt_auth_filter import JwtAuthFilter
from xflask.web.security.jwt_auth_manager import JwtAuthManager


class Application(object):
    DEF_CONF_FILE = 'conf/server.yml'

    DEF_LOG_FILE = 'conf/logging.yml'

    DEF_FILTERS = [JwtAuthFilter]

    DER_AUTH_MANAGER = JwtAuthManager

    DEF_ERROR_HANDLER = BasicErrorHandler

    def __init__(self, db, conf_files=None):
        self.db = db

        self.conf_files = conf_files or [get_file_path('main/conf/server.yml')]

        self.listeners = []

        self.components = []

        self.error_handler = self.DEF_ERROR_HANDLER

        self.filters = self.DEF_FILTERS

        self.auth_manager = self.DER_AUTH_MANAGER

        self.json_serializers = []

        self._pre_init()

    #### SETTER ####

    def set_filters(self, filters=[]):
        self.filters = filters

    def set_error_handler(self, error_handler):
        self.error_handler = error_handler

    def set_listeners(self, listeners=[]):
        self.listeners = listeners

    def set_auth_manager(self, auth_manager):
        self.auth_manager = auth_manager

    def register_json_serializer(self, serializer):
        self.json_serializers.append(serializer)

    def register_component(self, component):
        self.components.append(component)

    #### GETTER ####

    def get_component(self, clazz):
        component = self.flask_injector.injector.get(clazz)
        return None if type(component) == type else component

    #### RUN APP ####

    def run(self, host=None, port=None):
        host = host or self.conf.get('HOST')
        port = port or self.conf.get('PORT')

        self.app.run(host, port, use_reloader=False)

        self._on_stop()

    #### PRE INIT ####

    def _pre_init(self):
        self._init_config()

        self._init_logging()

        self._init_app()

        self._init_db()

        # register XFlask extension
        if not hasattr(self.app, 'extensions'):
            self.app.extensions = {}

        self.app.extensions['xflask'] = self

    def _init_config(self):
        self.conf = Configuration(get_xflask_path(self.DEF_CONF_FILE))
        for conf_file in self.conf_files:
            self.conf.merge(conf_file)

    def _init_logging(self):
        if self.conf.get('LOGGING') is False:
            logging.basicConfig(level=logging.DEBUG)
        else:
            self._logger = Logger(get_xflask_path(self.DEF_LOG_FILE))

            log_file = self.conf.get('LOGGING_CONF_FILE')
            if log_file is not None:
                self._logger.merge(log_file)

        self._logger = logging.getLogger(self.__class__.__name__)

    def _init_app(self):
        self.app = Flask(self.conf.get('APP_NAME'),
                         static_folder=self.conf.get('STATIC_DIR'),
                         template_folder=self.conf.get('TEMPLATE_DIR'),
                         root_path=get_root_dir())

        # config
        self.app.config.from_mapping(self.conf.cfg)

        # json encoder
        json_serializers = []
        json_serializers += JSON_SERIALIZERS
        json_serializers += self.json_serializers

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

    #### INIT ####

    def init(self):
        self._init_models()

        self._init_components()

        self._init_controllers()

        self._init_error_handler()

        self._init_filters()

        self._init_auth_manager()

        self._on_start()

    def _init_models(self):
        # TODO: nested packages
        import_modules(get_root_dir(), self.conf.get('MODEL') or [])

    def _init_components(self):

        def configure(binder):
            # config
            binder.bind(Configuration, self.conf, scope=singleton)

            # db
            if self.conf.exist('SQLALCHEMY_DATABASE_URI'):
                binder.bind(SQLAlchemy, to=self.db, scope=singleton)

            # components (registered manually)
            for obj in self.components:
                if issubclass(obj, Component):

                    if issubclass(obj, ApplicationStateListener):
                        self.listeners.append(obj)

                    scope = singleton if obj.scope == 'singleton' else request
                    binder.bind(obj, obj, scope)

        def configure_scan(binder):
            for package in self.conf.get('COMPONENT'):
                try:
                    self._logger.debug('>>> Scan modules in %s', package)

                    # TODO: nested packages
                    for pkg_name in find_modules(package):
                        try:
                            module = import_string(pkg_name)
                            class_names = [m[0] for m in inspect.getmembers(module, inspect.isclass) if
                                           m[1].__module__ == module.__name__]

                            valid_module = False
                            for class_name in class_names:
                                obj = getattr(module, class_name)

                                if issubclass(obj, Controller):
                                    continue

                                if issubclass(obj, ApplicationStateListener):
                                    self._component_listeners.append(obj)

                                if issubclass(obj, Component):
                                    if obj.abstract is True:
                                        continue

                                    valid_module = True

                                    scope = singleton if obj.scope == 'singleton' else request
                                    binder.bind(obj, obj, scope)

                                    self._logger.debug('Register component: %s', class_name)
                                else:
                                    del module
                                    self._logger.debug('!!! Invalid component: %s', class_name)

                            if not valid_module:
                                del module

                        except Exception as e:
                            self._logger.exception('!!! Failed to initialize component in %s', pkg_name, e)
                            sys.exit()

                except Exception:
                    self._logger.debug('!!! No modules founded in %s', package)

        self.flask_injector = FlaskInjector(app=self.app, modules=[configure, configure_scan])

    def _init_controllers(self):
        for package in self.conf.get('CONTROLLER'):
            try:
                self._logger.debug('>>> Scan modules in %s', package)

                # TODO: nested packages
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
                                    self._logger.exception('Failed to initialize controller: %s', class_name)
                                    sys.exit()

                                self._logger.debug('Register controller: %s', class_name)
                            else:
                                self._logger.debug('!!! Invalid controller: %s', class_name)

                        if not valid_module:
                            del module

                    except Exception as e:
                        self._logger.exception('!!! Failed to initialize controller in %s', module_ns, e)
                        sys.exit()

            except Exception:
                self._logger.debug('!!! No modules found in %s', package)

        # display registered routes
        self._logger.debug('>>> Registered routes:')

        routes = self.app.url_map._rules
        if routes is not None and len(routes) > 0:
            max_len = max([len(route.rule) for route in routes])
            for route in routes:
                self._logger.debug('%*s | %26s | %s', max_len, route.rule, route.methods, route.endpoint)

    def _init_error_handler(self):
        error_handler = self.error_handler
        if type(error_handler) == type and issubclass(error_handler, ErrorHandler):
            error_handler_ = self.get_component(error_handler)
            error_handler = error_handler() if error_handler_ is None else error_handler_

            self.error_handler = error_handler

        if isinstance(error_handler, ErrorHandler):
            error_handler.init(self)
        else:
            self._logger.debug('!!! Invalid error handler: %s', error_handler.__name__)

    def _init_filters(self):
        for idx, filter_ in enumerate(self.filters):
            if type(filter_) == type and issubclass(filter_, Filter):
                filter__ = self.get_component(filter_)
                filter_ = filter_() if filter__ is None else filter__

                self.filters[idx] = filter_

            if isinstance(filter_, Filter):
                filter_.init(self)

                self.app.before_request(filter_.before)
                self.app.after_request(filter_.after)
            else:
                self._logger.debug('!!! Invalid filter: %s', filter_.__name__)

    def _init_auth_manager(self):
        if self.auth_manager is None:
            return

        auth_manager = self.auth_manager
        if type(auth_manager) == type and issubclass(auth_manager, AuthManager):
            auth_manager_ = self.get_component(auth_manager)
            auth_manager = auth_manager() if auth_manager_ is None else auth_manager_

            self.auth_manager = auth_manager

        auth_manager.init(self)

    def _on_start(self):
        with self.app.app_context():
            for idx, listener in enumerate(self.listeners):
                if type(listener) == type and issubclass(listener, ApplicationStateListener):
                    listener_ = self.get_component(listener)
                    listener = listener() if listener_ is None else listener_

                    self.listeners[idx] = listener

                if isinstance(listener, ApplicationStateListener):
                    listener.on_start(self)
                else:
                    self._logger.debug('!!! Invalid application state listener: %s', listener.__name__)

    def _on_stop(self):
        with self.app.app_context():
            for listener in self.listeners:
                listener.on_stop(self)
