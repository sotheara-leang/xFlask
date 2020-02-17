from xflask.component import Component
from xflask.dao import Dao


class Service(Component):

    def __init__(self, dao: Dao):
        self.dao = dao

    def get_by_id(self, id):
        return self.dao.get_by_id(id)

    def get_all(self):
        return self.dao.get_all()

    def query(self):
        return self.dao.query()

    def create(self, obj):
        self.dao.insert(obj)

    def update(self, obj):
        self.dao.update(obj)

    def delete(self, obj):
        self.dao.delete(obj)

    def delete_by_id(self, id):
        self.dao.delete_by_id(id)

    def begin(self, subtransactions=True, nested=False):
        self.dao.begin(subtransactions=subtransactions, nested=nested)

    def begin_nested(self):
        self.db.begin_nested()

    def flush(self, objs):
        self.dao.flush(objs)

    def commit(self):
        self.dao.commit()

    def rollback(self):
        self.dao.rollback()
