from flask_sqlalchemy.model import DefaultMeta

from xflask.component import Component
from xflask.dao import Dao


class Service(Component):
    ...


class CrudService(Service):

    def __init__(self, dao: Dao):
        if isinstance(dao, DefaultMeta):
            self.dao = Dao(dao)
        elif isinstance(dao, Dao):
            self.dao = dao
        else:
            raise Exception('Invalid dao')

    def exist(self, id=None, **criterion):
        return self.dao.exist(id, **criterion)

    def get(self, id=None, **criterion):
        return self.dao.get(id, **criterion)

    def get_all(self, **criterion):
        return self.dao.get_all(**criterion)

    def query(self, *models):
        return self.dao.query(*models)

    def insert(self, obj):
        self.dao.insert(obj)

    def update(self, obj, **criterion):
        self.dao.update(obj, **criterion)

    def delete(self, obj=None, **criterion):
        self.dao.delete(obj, **criterion)

    def delete_all(self):
        self.dao.delete_all()

    def _begin(self, subtransactions=True, nested=False):
        self.dao.begin(subtransactions=subtransactions, nested=nested)

    def _begin_nested(self):
        self.dao.begin_nested()

    def _flush(self, objs):
        self.dao.flush(objs)

    def _merge(self, obj):
        return self.dao.merge(obj)

    def _commit(self):
        self.dao.commit()

    def _rollback(self):
        self.dao.rollback()
