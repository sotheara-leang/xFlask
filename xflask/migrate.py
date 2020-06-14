import importlib
import logging
import sys

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from xflask.common.util import scan_namespaces
from xflask.sqlalchemy import db


class Migration(object):

    def __init__(self, application, **args):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.application = application

        migration = application.get_property('MIGRATION')

        migration_dir = migration['DIR']
        model_namespaces = migration['MODEL'] or []

        for model_namespace in model_namespaces:
            namespaces = scan_namespaces(model_namespace)
            for namespace in namespaces:
                try:
                    importlib.import_module(namespace)
                except Exception as e:
                    self.logger.exception('!!! Failed to initialize model in %s', namespace, e)

                    sys.exit()

        self.migrate = Migrate(application.app, db, directory=migration_dir, **args)

        self.manager = Manager(application.app)
        self.manager.add_command('db', MigrateCommand)

    def run(self):
        self.manager.run()
