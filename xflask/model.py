from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func

from xflask import db
from xflask.type import Enum
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
            elif isinstance(value, Enum):
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
                        elif isinstance(value, Enum):
                            value = value.code()

                        ret_data[key] = value

        return ret_data

    def from_dict(self, **kwargs):
        _force = kwargs.pop("_force", False)

        readonly = self._readonly_fields if hasattr(self, "_readonly_fields") else []
        readonly += ['id', 'created_at', 'created_by', 'modified_at', 'modified_by', 'deleted_at', 'deleted_by']

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        changes = {}

        # fields
        for key in columns:
            if key.startswith("_"):
                continue

            allowed = True if _force or key not in readonly else False
            exists = True if key in kwargs else False
            if allowed and exists:
                val = getattr(self, key)
                if val != kwargs[key]:
                    changes[key] = {"old": val, "new": kwargs[key]}
                    setattr(self, key, kwargs[key])

        # relationships
        for rel in relationships:
            if key.startswith("_"):
                continue

            allowed = True if _force or rel not in readonly else False
            exists = True if rel in kwargs else False
            if allowed and exists:
                is_list = self.__mapper__.relationships[rel].uselist
                if is_list:
                    valid_ids = []
                    query = getattr(self, rel)
                    cls = self.__mapper__.relationships[rel].argument()
                    for item in kwargs[rel]:
                        if (
                                "id" in item
                                and query.filter_by(id=item["id"]).limit(1).count() == 1
                        ):
                            obj = cls.query.filter_by(id=item["id"]).first()
                            col_changes = obj.from_dict(**item)
                            if col_changes:
                                col_changes["id"] = str(item["id"])
                                if rel in changes:
                                    changes[rel].append(col_changes)
                                else:
                                    changes.update({rel: [col_changes]})
                            valid_ids.append(str(item["id"]))
                        else:
                            col = cls()
                            col_changes = col.from_dict(**item)
                            query.append(col)
                            db.session.flush()
                            if col_changes:
                                col_changes["id"] = str(col.id)
                                if rel in changes:
                                    changes[rel].append(col_changes)
                                else:
                                    changes.update({rel: [col_changes]})
                            valid_ids.append(str(col.id))

                    # delete rows from relationship that were not in kwargs[rel]
                    for item in query.filter(not (cls.id.in_(valid_ids))).all():
                        col_changes = {"id": str(item.id), "deleted": True}
                        if rel in changes:
                            changes[rel].append(col_changes)
                        else:
                            changes.update({rel: [col_changes]})
                        db.session.delete(item)

                else:
                    val = getattr(self, rel)
                    if self.__mapper__.relationships[rel].query_class is not None:
                        if val is not None:
                            col_changes = val.from_dict(**kwargs[rel])
                            if col_changes:
                                changes.update({rel: col_changes})
                    else:
                        if val != kwargs[rel]:
                            setattr(self, rel, kwargs[rel])
                            changes[rel] = {"old": val, "new": kwargs[rel]}

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            allowed = True if _force or key not in readonly else False
            exists = True if key in kwargs else False
            if allowed and exists and getattr(self.__class__, key).fset is not None:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    val = val.to_dict()
                changes[key] = {"old": val, "new": kwargs[key]}
                setattr(self, key, kwargs[key])

        return changes

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
