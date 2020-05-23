from xflask.component import Component
from xflask.sqlalchemy import db, transactional


class Dao(Component):

    def __init__(self, model):
        self.model = model
        self.db.session = db.session

    def exist(self, id=None, **criterion):
        query =  self.query().filter_by(**self._get_pk_criterion(id)) \
            if id is not None else self.query().filter_by(**criterion)
        return query.scalar() is not None

    def get(self, id=None, **criterion):
        return self.query().filter_by(**self._get_pk_criterion(id)).first() \
            if id is not None else self.query().filter_by(**criterion).first()

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
    def update(self, obj, **criterion):
        if len(criterion) > 0:
            self.query().filter_by(**criterion).update(obj if isinstance(obj, dict) else obj.to_dict())
        elif isinstance(obj, dict):
            self.query().filter_by(**self._get_pk_criterion(obj)).update(obj)

    @transactional()
    def delete(self, obj=None, **criterion):
        if len(criterion) > 0:
            self.query().filter_by(**criterion).delete()
        elif obj is not None:
            if isinstance(obj, (int, float)) or isinstance(obj, tuple):
                self.query().filter_by(**self._get_pk_criterion(obj)).delete()
            else:
                db.session.delete(obj)
    
    def _begin(self, subtransactions=True, nested=False):
        db.session.begin(subtransactions=subtransactions, nested=nested)

    def _begin_nested(self):
        db.session.begin_nested()

    def _flush(self, objs):
        db.session.flush(objs)

    def _merge(self, obj):
        return db.session.merge(obj)

    def _commit(self):
        db.session.commit()

    def _rollback(self):
        db.session.rollback()
        
    def _get_pk_criterion(self, id):
        if isinstance(id, (int, float)):
            id = (id,)

        criterion = {}
        for idx, pk in enumerate(self.model.__mapper__.primary_key):
            criterion[pk.name] = id[idx]

        return criterion
