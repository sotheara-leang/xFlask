from xflask.common.util import to_dict
from xflask.component import Component
from xflask.sqlalchemy import db, transactional


class Dao(Component):

    def __init__(self, model):
        self.session = db.session
        self.model = model

    def count(self):
        return self.query().count()

    def count_by_filter(self, **filter):
        return self.query().filter_by(**filter).count()

    def exist(self, id):
        return self.query().filter_by(**self.get_pk_filter(id)).scalar() is not None

    def exist_by_filter(self, **filter):
        return self.query().filter_by(**filter).scalar() is not None

    def get(self, id):
        return self.query().filter_by(**self.get_pk_filter(id)).first()

    def get_by_filter(self, **filter):
        return self.query().filter_by(**filter).first()

    def get_all(self):
        return self.query().all()

    def get_all_by_filter(self, sort=(), **filter):
        return self.query().filter_by(**filter).order_by(*sort).all()

    def get_page(self, page=1, per_page=30):
        return self.query().paginate(page, per_page=per_page)

    def get_page_by_filter(self, page=1, per_page=30, sort=(), **filter):
        filter = init_filter(**filter)

        return self.query().filter_by(**filter).order_by(*sort).paginate(page, per_page=per_page)

    def query(self, *models):
        if models is None or len(models) == 0:
            return self.session.query(self.model)
        else:
            return self.session.query(*models)

    @transactional()
    def insert(self, obj):
        if isinstance(obj, dict):
            obj = self.model(**obj)

        self.session.add(obj)

    @transactional()
    def insert_all(self, objs):
        self.session.add_all(objs)

    @transactional()
    def update(self, obj):
        if isinstance(obj, dict):
            self.query().filter_by(**self.get_pk_filter_by_object(obj)).update(obj)
        else:
            self.session.merge(obj)

    @transactional()
    def update_by_filter(self, obj, **filter):
        self.query().filter_by(**filter).update(obj if isinstance(obj, dict) else to_dict(obj))

    @transactional()
    def delete(self, obj):
        if isinstance(obj, (int, float)) or isinstance(obj, tuple):
            self.query().filter_by(**self.get_pk_filter(obj)).delete()
        else:
            self.session.delete(obj)

    def delete_by_filter(self, **filter):
        self.query().filter_by(**filter).delete()

    def delete_all(self):
        self.query().delete()

    def get_pk_filter(self, id):
        if isinstance(id, (int, float)):
            id = (id,)

        filter = {}
        for idx, pk in enumerate(self.model.__mapper__.primary_key):
            filter[pk.name] = id[idx]

        return filter

    def get_pk_filter_by_object(self, obj):
        filter = {}
        for idx, pk in enumerate(self.model.__mapper__.primary_key):
            filter[pk.name] = obj[pk.name]

        return filter


def init_filter(**criterion):
    ret_dict = {}
    for field, value in criterion.items():
        if value is not None:
            ret_dict[field] = value
    return ret_dict
