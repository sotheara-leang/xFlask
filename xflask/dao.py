from injector import inject
from flask_sqlalchemy import SQLAlchemy

from xflask.component import Component


class Dao(Component):

    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def add(self, obj):
        self.db.session.add(obj)

    def delete(self, obj):
        self.db.session.delete(obj)

    def commit(self):
        self.db.session.commit()
