from .component import Component
from .dao import Dao


class Service(Component):

    def __init__(self, dao: Dao):
        self.dao = dao

    def get_by_id(self, id):
        return self.dao.get_by_id(id)

    def get_all(self):
        return self.dao.get_all()

    def create(self, obj):
        self.dao.insert(obj)

    def update(self, obj):
        self.dao.update(obj)

    def delete(self, obj):
        self.dao.delete(obj)

    def delete_by_id(self, id):
        self.dao.delete_by_id(id)


