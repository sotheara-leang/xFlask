from xflask import db
from xflask.model.serializer import EnumSerializer, DateTimeSerializer


class Model(db.Model):
    __abstract__ = True

    _type_decorators = [EnumSerializer(), DateTimeSerializer()]

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

            # decorator
            if serialize is True:
                for decorator in self._type_decorators:
                    if decorator.accept(value):
                        value = decorator.serialize(value)
                        break

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

                        # decorator
                        if serialize is True:
                            for decorator in self._type_decorators:
                                if decorator.accept(value):
                                    value = decorator.serialize(value)
                                    break

                    ret_data[key] = value

        return ret_data

