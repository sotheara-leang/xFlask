class Vo(object):

    @classmethod
    def validate(cls, obj: dict):
        return cls.schema().validate(obj)

    @classmethod
    def load(cls, obj: dict):
        return cls(**cls.schema().load(obj))

    @classmethod
    def schema(cls):
        pass
