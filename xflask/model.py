from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func

from xflask import db
from xflask.type import Type
from xflask.security import get_current_user
from xflask.common.date_util import *


class Model(db.Model):
    __abstract__ = True

    def to_dict(self, show=[], hide=[], dept=0, df=dd_MM_yyyy_hh_mm_ss):
        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
        hidden.extend([e for e in hide if '.' not in e])
        hidden = [e for e in hidden if e not in show]

        ret_data = {}

        # fields
        columns = self.__table__.columns.keys()
        for key in columns:
            if key.startswith("_") or key in hidden:
                continue

            value = getattr(self, key)
            if isinstance(value, datetime):
                value = to_date_str(value, df)
            elif isinstance(value, Type):
                value = value.code()

            ret_data[key] = value

        # relationships
        if dept > 0:
            relationships = self.__mapper__.relationships.keys()
            for key in relationships:
                if key.startswith("_") or key in hidden:
                    continue

                _show = [e.split('.')[1] for e in show if e.split('.')[0] == key]
                _hide = [e.split('.')[1] for e in hide if e.split('.')[0] == key]

                is_list = self.__mapper__.relationships[key].uselist
                if is_list:
                    items = getattr(self, key)
                    if self.__mapper__.relationships[key].query_class is not None:
                        if hasattr(items, "all"):
                            items = items.all()

                    ret_data[key] = []

                    for item in items:
                        ret_data[key].append(
                            item.to_dict(
                                show=list(_show),
                                hide=list(_hide),
                                dept=dept - 1
                            )
                        )
                else:
                    if (
                            self.__mapper__.relationships[key].query_class is not None
                            or self.__mapper__.relationships[key].instrument_class
                            is not None
                    ):
                        item = getattr(self, key)
                        if item is not None:
                            ret_data[key] = item.to_dict(
                                show=list(_show),
                                hide=list(_hide),
                                dept=dept - 1
                            )
                        else:
                            ret_data[key] = None
                    else:
                        value = getattr(self, key)
                        if isinstance(value, datetime):
                            value = to_date_str(value, df)
                        elif isinstance(value, Type):
                            value = value.code()

                        ret_data[key] = value

        return ret_data


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
        return db.Column(db.Integer, db.ForeignKey('user.id'))

    @staticmethod
    def before_delete(mapper, connection, instance):
        user = get_current_user() or {}
        instance.deleted_at = func.now()
        instance.deleted_by = user.get('id')

    @classmethod
    def __declare_last__(cls):
        db.event.listen(cls, 'before_delete', cls.before_delete)
