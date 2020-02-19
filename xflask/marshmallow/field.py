from marshmallow import fields
from xflask.type import Enum


class Enum(fields.Field):

    def __init__(self, enum_type: Enum, **kwargs):
        super().__init__(**kwargs)
        self.enum_type = enum_type

    def _serialize(self, value, attr, obj, **kwargs):
        return value.code()

    def _deserialize(self, value, attr, data, **kwargs):
        super()._deserialize(value, attr, data, **kwargs)
        return self.enum_type.value_of(value)
