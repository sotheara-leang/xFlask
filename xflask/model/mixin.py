from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func

from xflask import db
from xflask.web.security import get_current_user


class AuditableMixin:
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    @declared_attr
    def created_by(cls):
        return db.Column(db.Integer)

    @declared_attr
    def modified_by(cls):
        return db.Column(db.Integer)

    @staticmethod
    def before_insert(mapper, connection, instance):
        user = get_current_user() or {}
        instance.created_at = func.now()
        instance.created_by = user.get('id')

    @staticmethod
    def before_update(mapper, connection, instance):
        user = get_current_user() or {}
        instance.modified_at = func.now()
        instance.modified_by = user.get('id')

    @classmethod
    def __declare_last__(cls):
        db.event.listen(cls, 'before_insert', cls.before_insert)
        db.event.listen(cls, 'before_update', cls.before_insert)


class SoftableMixin:
    deleted_at = db.Column(db.DateTime)

    @declared_attr
    def deleted_by(cls):
        return db.Column(db.Integer)

    @staticmethod
    def before_delete(mapper, connection, instance):
        user = get_current_user() or {}
        instance.deleted_at = func.now()
        instance.deleted_by = user.get('id')

    @classmethod
    def __declare_last__(cls):
        db.event.listen(cls, 'before_delete', cls.before_delete)
