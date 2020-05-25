import marshmallow.schema

from marshmallow import EXCLUDE, ValidationError


class Schema(object):

    def __init__(self, *args, **kwargs):
        if not hasattr(self.__class__, '__annotations__'):
            return

        if args is not None and len(args) > 0:
            for idx, name in enumerate(self.__annotations__.keys()):
                value = None if idx >= len(args) else args[idx]
                self.__dict__[name] = value
        else:
            for name in self.__annotations__.keys():
                value = kwargs.get(name)
                self.__dict__[name] = value

    @staticmethod
    def _get_schema(cls, exclude=[]):
        if not hasattr(cls, '__annotations__'):
            raise Exception(cls.__name__ + ' has no annotations')

        annotations_map = {}

        annotations = cls.__annotations__
        for name, annotation in annotations.items():
            if name in exclude:
                continue
            annotations_map[name] = annotation

        if len(exclude) > 0:
            return marshmallow.Schema.from_dict(annotations_map)(unknown=EXCLUDE)
        else:
            return marshmallow.Schema.from_dict(annotations_map)()

    @classmethod
    def validate(cls, obj: dict, exclude=[]):
        schema = cls._get_schema(exclude)
        result = schema.validate(obj)
        try:
            cls.custom_validate(obj, exclude)
        except ValidationError:
            result = False

        return result

    @classmethod
    def serialize(cls, obj, exclude=[]):
        schema = cls._get_schema(exclude)
        return schema.dump(obj)

    def serialize_(self, exclude=[]):
        schema = self.__class__._get_schema(exclude)
        return schema.dump(self)

    @classmethod
    def deserialize(cls, obj: dict, exclude=[]):
        schema = cls._get_schema(exclude)
        data = cls._load(schema, obj, exclude)
        return cls(**data)

    @classmethod
    def deserialize_as_dict(cls, obj: dict, exclude=[]):
        schema = cls._get_schema(exclude)
        return cls._load(schema, obj, exclude)

    def deserialize_(self, obj: dict, exclude=[]):
        schema = self.__class__._get_schema(exclude)
        data = self._load(schema, obj, exclude)
        return self.__class__(**data)

    @classmethod
    def _load(cls, schema, obj, exclude):
        data = schema.load(obj)

        # perform custom validation
        cls.custom_validate(obj, exclude)

        return data

    @staticmethod
    def custom_validate(data, exclude):
        pass
