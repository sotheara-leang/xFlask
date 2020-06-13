from flask_sqlalchemy.model import DefaultMeta

from xflask.component import Component
from xflask.dao import Dao
from xflask.sqlalchemy import db


class Service(Component):
    ...


class PersistenceService(Service):

    def __init__(self, dao: Dao = None):
        if dao is not None:
            if isinstance(dao, DefaultMeta):
                self.dao = Dao(dao)
            elif isinstance(dao, Dao):
                self.dao = dao
            else:
                raise Exception('Invalid dao: ', dao.__class__.__name__)

        self.session = db.session


class CrudService(PersistenceService):

    def __init__(self, dao: Dao):
        super(CrudService, self).__init__(dao)

    def count(self):
        return self.dao.count()

    def count_by_filter(self, **filter):
        return self.dao.count_by_filter(**filter)

    def exist(self, id):
        return self.dao.exist(id)

    def exist_by_filter(self, **filter):
        return self.dao.exist_by_filter(**filter)

    def get(self, id):
        return self.dao.get(id)

    def get_by_filter(self, **filter):
        return self.dao.get_by_filter(**filter)

    def get_all(self):
        return self.dao.get_all()

    def get_all_by_filter(self, sort=(), **filter):
        return self.get_all_by_filter(sort, **filter)

    def get_page(self, page=1, per_page=30):
        return self.dao.get_page(page, per_page)

    def get_page_by_filter(self, page=1, per_page=30, sort=(), **filter):
        return self.dao.get_page_by_filter(page, per_page, sort, **filter)

    def query(self, *models):
        return self.dao.query(*models)

    def create(self, obj):
        self.dao.insert(obj)

    def update(self, obj):
        self.dao.update(obj)

    def update_by_filter(self, obj, **filter):
        self.update_by_filter(obj, **filter)

    def delete(self, obj):
        self.dao.delete(obj)

    def delete_by_filter(self, **filter):
        self.dao.delete_by_filter(**filter)

    def delete_all(self):
        self.dao.delete_all()
