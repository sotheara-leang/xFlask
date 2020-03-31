import enum
from datetime import datetime

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func

from xflask.common.util.date_util import to_date_str
from xflask.sqlalchemy import db
from xflask.type.enum import Enum
from xflask.web.security import get_current_user


class Model(db.Model):
    __abstract__ = True

    def serialize(self, show=[], hide=[], dept=0):
        return self.to_dict(show, hide, dept, True)

    def to_dict(self, show=[], hide=[], dept=0, serialize=False):
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
            if serialize is True:
                value = self._custom_serialization(value)

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
                        if serialize is True:
                            value = self._custom_serialization(value)

                    ret_data[key] = value

        return ret_data

    def _custom_serialization(self, obj):
        if isinstance(obj, Enum):
            return obj.code()
        elif isinstance(obj, enum.Enum):
            return obj.value
        elif isinstance(obj, datetime):
            return to_date_str(obj)
        else:
            return obj


class AuditModel(Model):
    __abstract__ = True

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


class SoftModel:
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
