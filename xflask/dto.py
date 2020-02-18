from marshmallow import Schema


class Dto(object):

    @classmethod
    def validate(cls, obj: dict):
        return Schema.from_dict(cls.schema())().validate(obj)

    @classmethod
    def load(cls, obj: dict):
        result = Schema.from_dict(cls.schema())().load(obj)
        return cls(**result)

    @classmethod
    def load_as_dict(cls, obj: dict):
        return Schema.from_dict(cls.schema())().load(obj)

    @classmethod
    def schema(cls):
        pass
