from xflask.component import Component
from xflask.sqlalchemy import session, transactional


class Dao(Component):

    def __init__(self, model):
        self.model = model

    def count(self, **criterion):
        return self.query().filter_by(**criterion).count()

    def exist(self, id=None, **criterion):
        query = self.query().filter_by(**self._get_pk_criterion(id)) \
            if id is not None else self.query().filter_by(**criterion)
        return query.scalar() is not None

    def get(self, id=None, **criterion):
        return self.query().filter_by(**self._get_pk_criterion(id)).first() \
            if id is not None else self.query().filter_by(**criterion).first()

    def get_all(self, order=(), **criterion):
        return self.query().filter_by(**criterion).order_by(*order).all()

    def get_page(self, page=1, per_page=30, order=(), **criterion):
        criterion = filter_criterion(**criterion)

        return self.query().filter_by(**criterion).order_by(*order).paginate(page, per_page=per_page)

    def query(self, *models):
        if models is None or len(models) == 0:
            return session.query(self.model)
        else:
            return session.query(*models)

    @transactional()
    def insert(self, obj):
        if isinstance(obj, dict):
            obj = self.model(**obj)

        session.add(obj)

    @transactional()
    def update(self, obj, **criterion):
        if len(criterion) > 0:
            self.query().filter_by(**criterion).update(obj if isinstance(obj, dict) else obj.to_dict())
        elif isinstance(obj, dict):
            self.query().filter_by(**self._get_pk_criterion_by_object(obj)).update(obj)
        else:
            self._merge(obj)

    @transactional()
    def delete(self, obj=None, **criterion):
        if len(criterion) > 0:
            self.query().filter_by(**criterion).delete()
        elif obj is not None:
            if isinstance(obj, (int, float)) or isinstance(obj, tuple):
                self.query().filter_by(**self._get_pk_criterion_by_object(obj)).delete()
            else:
                session.delete(obj)

    def delete_all(self):
        self.query().delete()

    def _begin(self, subtransactions=True, nested=False):
        session.begin(subtransactions=subtransactions, nested=nested)

    def _begin_nested(self):
        session.begin_nested()

    def _flush(self, objs):
        session.flush(objs)

    def _merge(self, obj):
        return session.merge(obj)

    def _commit(self):
        session.commit()

    def _rollback(self):
        session.rollback()

    def _get_pk_criterion(self, id):
        if isinstance(id, (int, float)):
            id = (id,)

        criterion = {}
        for idx, pk in enumerate(self.model.__mapper__.primary_key):
            criterion[pk.name] = id[idx]

        return criterion

    def _get_pk_criterion_by_object(self, obj):
        criterion = {}
        for idx, pk in enumerate(self.model.__mapper__.primary_key):
            criterion[pk.name] = obj[pk.name]

        return criterion

def filter_criterion(**criterion):
    ret_dict = {}
    for field, value in criterion.items():
        if value is not None:
            ret_dict[field] = value
    return ret_dict
