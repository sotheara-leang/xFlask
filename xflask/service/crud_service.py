from xflask.service import Service
from xflask.dao import Dao


class CrudService(Service):

    def __init__(self, dao: Dao):
        self.dao = dao

    def exist(self, id):
        return self.dao.exist(id)

    def get(self, id):
        return self.dao.get(id)

    def get_all(self):
        return self.dao.get_all()

    def query(self, models):
        return self.dao.query(models)

    def create(self, obj):
        self.dao.insert(obj)

    def update(self, obj):
        self.dao.update(obj)

    def delete(self, obj):
        self.dao.delete(obj)

    def begin(self, subtransactions=True, nested=False):
        self.dao.begin(subtransactions=subtransactions, nested=nested)

    def begin_nested(self):
        self.dao.begin_nested()

    def flush(self, objs):
        self.dao.flush(objs)

    def commit(self):
        self.dao.commit()

    def rollback(self):
        self.dao.rollback()
