from flask_sqlalchemy import SQLAlchemy

from xflask.component import Component
from xflask.decorator import transactional


class Dao(Component):

    def __init__(self, model, db: SQLAlchemy):
        self.model = model
        self.db = db

    def get_by_id(self, id):
        return self.query().get(id)

    def get_all(self):
        return self.query().all()

    def query(self):
        return self.db.session.query(self.model)

    @transactional()
    def insert(self, obj):
        self.db.session.add(obj)

    @transactional()
    def update(self, obj):
        self.query().filter_by(id=obj.id).update(obj.to_dict(json_serialize=False))

    @transactional()
    def delete(self, obj):
        self.db.session.delete(obj)

    @transactional()
    def delete_by_id(self, id):
        self.query().filter_by(id=id).delete()

    def begin(self, subtransactions=True, nested=False):
        self.db.session.begin(subtransactions=subtransactions, nested=nested)

    def begin_nested(self):
        self.db.session.begin_nested()

    def flush(self, objs):
        self.db.session.flush(objs)

    def commit(self):
        self.db.session.commit()

    def rollback(self):
        self.db.session.rollback()
