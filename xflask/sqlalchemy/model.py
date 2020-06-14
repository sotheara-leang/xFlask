from datetime import datetime

from flask import json
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm.attributes import QueryableAttribute

from xflask.sqlalchemy import db
from xflask.web.security import get_current_user


class Model(db.Model):
    __abstract__ = True

    @classmethod
    def get_column(cls, col_name):
        return cls.__table__.columns.get(col_name)

    @classmethod
    def get_sort_expression(cls, col_name, sort='asc'):
        column = cls.get_column(col_name)
        if column is None:
            return None

        return column.asc() if sort == 'asc' else column.desc()

    def to_dict(self, show=[], _hide=[], _path=None):
        """Return a dictionary representation of this model."""

        hidden = self._hidden_columns if hasattr(self, '_hidden_columns') else []
        hidden = list(set(hidden) | set(_hide) - set(show))

        if not _path:
            _path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()

                if item.split('.', 1)[0] == _path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != '.':
                    item = '.%s' % item

                item = '%s%s' % (_path, item)

                return item

            show[:] = [prepend_path(x) for x in show]
            _hide[:] = [prepend_path(x) for x in _hide]

        ret_data = {}

        #### columns  ####

        columns = self.__table__.columns.keys()
        for key in columns:
            if key.startswith('_'):
                continue

            check = '%s.%s' % (_path, key)
            if check in _hide or key in hidden:
                continue

            ret_data[key] = getattr(self, key)

        #### relationships ####

        unloaded_relationships = inspect(self).unloaded
        relationships = self.__mapper__.relationships.keys()
        for key in relationships:
            if key.startswith('_'):
                continue

            check = '%s.%s' % (_path, key)
            if check in _hide or key in hidden or key in unloaded_relationships:
                continue

            # _hide.append(check)

            is_list = self.__mapper__.relationships[key].uselist
            if is_list:
                items = getattr(self, key)
                if self.__mapper__.relationships[key].query_class is not None:
                    if hasattr(items, 'all'):
                        items = items.all()

                ret_data[key] = []
                for item in items:
                    ret_data[key].append(
                        item.to_dict(
                            show=list(show),
                            _hide=list(_hide),
                            _path=('%s.%s' % (_path, key.lower()))
                        )
                    )
            else:
                if (
                        self.__mapper__.relationships[key].query_class is not None
                        or self.__mapper__.relationships[key].instrument_class is not None
                ):
                    item = getattr(self, key)
                    if item is not None:
                        ret_data[key] = item.to_dict(
                            show=list(show),
                            _hide=list(_hide),
                            _path=('%s.%s' % (_path, key.lower()))
                        )
                    else:
                        ret_data[key] = None
                else:
                    ret_data[key] = getattr(self, key)

        #### properties ####

        properties = dir(self)
        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith('_'):
                continue
            if not hasattr(self.__class__, key):
                continue

            attr = getattr(self.__class__, key)
            if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
                continue

            check = '%s.%s' % (_path, key)
            if check in _hide or key in hidden:
                continue

            val = getattr(self, key)
            if hasattr(val, 'to_dict'):
                ret_data[key] = val.to_dict(
                    show=list(show),
                    _hide=list(_hide),
                    _path=('%s.%s' % (_path, key.lower()))
                )
            else:
                try:
                    ret_data[key] = json.loads(json.dumps(val))
                except Exception:
                    pass

        return ret_data

    def from_dict(self, **kwargs):
        """Update this model with a dictionary."""

        readonly = self._readonly_columns if hasattr(self, '_readonly_columns') else []
        if hasattr(self, '_hidden_columns'):
            readonly += self._hidden_columns

        #### columns ####

        columns = self.__table__.columns.keys()
        for key in columns:
            if key.startswith('_'):
                continue

            allowed = True if key not in readonly else False
            exists = True if key in kwargs else False
            if allowed and exists:
                setattr(self, key, kwargs[key])

        #### relationships ####

        relationships = self.__mapper__.relationships.keys()
        for rel in relationships:
            if rel.startswith('_'):
                continue

            allowed = True if rel not in readonly else False
            exists = True if rel in kwargs else False
            if allowed and exists:
                is_list = self.__mapper__.relationships[rel].uselist
                if is_list:
                    cls = self.__mapper__.relationships[rel].argument()

                    obj_list = []
                    for item in kwargs[rel]:
                        obj = cls()
                        obj.from_dict(**item)
                        obj_list.append(obj)

                    setattr(self, rel, obj_list)
                else:
                    cls = self.__mapper__.relationships[rel].argument._identity_class

                    obj = cls()
                    obj.from_dict(**kwargs[rel])

                    setattr(self, rel, obj)

        #### properties ####

        properties = dir(self)
        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith('_'):
                continue

            allowed = True if key not in readonly else False
            exists = True if key in kwargs else False
            if allowed and exists:
                setattr(self, key, kwargs[key])

    def from_dict_with_merge_state(self, **kwargs):
        """Update this state model with a dictionary."""

        _force = kwargs.pop("_force", False)

        readonly = self._readonly_columns if hasattr(self, '_readonly_columns') else []
        if hasattr(self, '_hidden_columns'):
            readonly += self._hidden_columns

        changes = {}

        #### columns ####

        columns = self.__table__.columns.keys()
        for key in columns:
            if key.startswith('_'):
                continue
            allowed = True if _force or key not in readonly else False
            exists = True if key in kwargs else False
            if allowed and exists:
                val = getattr(self, key)
                if val != kwargs[key]:
                    changes[key] = {'old': val, 'new': kwargs[key]}
                    setattr(self, key, kwargs[key])

        #### relationships ####

        relationships = self.__mapper__.relationships.keys()
        for rel in relationships:
            if rel.startswith('_'):
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
                                'id' in item
                                and query.filter_by(id=item['id']).limit(1).count() == 1
                        ):
                            obj = cls.query.filter_by(id=item['id']).first()
                            col_changes = obj.from_dict(**item)
                            if col_changes:
                                col_changes['id'] = str(item['id'])
                                if rel in changes:
                                    changes[rel].append(col_changes)
                                else:
                                    changes.update({rel: [col_changes]})
                            valid_ids.append(str(item['id']))
                        else:
                            col = cls()
                            col_changes = col.from_dict(**item)
                            query.append(col)
                            db.session.flush()
                            if col_changes:
                                col_changes['id'] = str(col.id)
                                if rel in changes:
                                    changes[rel].append(col_changes)
                                else:
                                    changes.update({rel: [col_changes]})
                            valid_ids.append(str(col.id))

                    # delete rows from relationship that were not in kwargs[rel]
                    for item in query.filter(not (cls.id.in_(valid_ids))).all():
                        col_changes = {'id': str(item.id), 'deleted': True}
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
                            changes[rel] = {'old': val, 'new': kwargs[rel]}

        #### properties ####

        properties = dir(self)
        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith('_'):
                continue
            allowed = True if _force or key not in readonly else False
            exists = True if key in kwargs else False
            if allowed and exists and getattr(self.__class__, key).fset is not None:
                val = getattr(self, key)
                if hasattr(val, 'to_dict'):
                    val = val.to_dict()
                changes[key] = {'old': val, 'new': kwargs[key]}
                setattr(self, key, kwargs[key])

        return changes


class TrackModel(Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, onupdate=datetime.now)


class AuditModel(TrackModel):
    __abstract__ = True

    @declared_attr
    def created_by(self):
        return db.Column(db.Integer, default=_current_user_id_or_none)

    @declared_attr
    def modified_by(self):
        return db.Column(db.Integer, onupdate=_current_user_id_or_none)


class SoftModel(AuditModel):
    __abstract__ = True

    deleted_at = db.Column(db.DateTime)

    @declared_attr
    def deleted_by(self):
        return db.Column(db.Integer)

    def set_soft_columns(self):
        self.deleted_at = datetime.now()
        self.deleted_by = _current_user_id_or_none()

    def is_soft(self):
        return self.deleted_at is not None


def _current_user_id_or_none():
    user = get_current_user() or {}
    return user.get('id')
