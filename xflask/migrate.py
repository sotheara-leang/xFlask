from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from xflask.common.util import get_root_dir, import_modules
from xflask.sqlalchemy import db


class Migration(object):

    def __init__(self, server, model_pkgs=[], **args):
        self.server = server
        self.migrate = Migrate(server.app, db, directory='migration', **args)

        self.manager = Manager(server.app)
        self.manager.add_command('db', MigrateCommand)

        import_modules(get_root_dir(), model_pkgs)

    def run(self):
        self.manager.run()
