from xflask.common.util.obj_util import to_dict
from xflask.component import Component
from xflask.sqlalchemy import db, transactional


class Dao(Component):

    def __init__(self, model):
        self.model = model

    def exist(self, id, **criterion):
        filter_ =  self.query().filter_by(id=id) if id is not None else self.query().filter_by(**criterion)
        return filter_.scalar() is not None

    def get(self, id=None, **criterion):
        return self.query().get(id) if id is not None else self.query().filter_by(**criterion).first()

    def get_all(self, **criterion):
        return self.query().filter_by(**criterion).all()

    def query(self, *models):
        if models is None or len(models) == 0:
            return db.session.query(self.model)
        else:
            return db.session.query(*models)

    @transactional()
    def insert(self, obj):
        if isinstance(obj, dict):
            obj = self.model(**obj)

        db.session.add(obj)

    @transactional()
    def update(self, obj):
        if isinstance(obj, dict):
            self.query().filter_by(id=obj['id']).update(obj)
        else:
            self.query().filter_by(id=obj.id).update(to_dict(obj))

    @transactional()
    def delete(self, obj):
        if isinstance(obj, (int, float)):
            self.query().filter_by(id=obj).delete()
        else:
            db.session.delete(obj)

    def begin(self, subtransactions=True, nested=False):
        db.session.begin(subtransactions=subtransactions, nested=nested)

    def begin_nested(self):
        db.session.begin_nested()

    def flush(self, objs):
        db.session.flush(objs)

    def merge(self, obj):
        return db.session.merge(obj)

    def commit(self):
        db.session.commit()

    def rollback(self):
        db.session.rollback()
