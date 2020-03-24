import sqlalchemy.types as types

from xflask.type import Enum


class StringEnum(types.TypeDecorator):
    impl = types.String

    def __init__(self, enum_type: Enum, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enum_type = enum_type

    def process_bind_param(self, value, dialect):
        return None if value is None else value.code()

    def process_result_value(self, value, dialect):
        return self.enum_type.value_of(value)


class IntegerEnum(StringEnum):
    impl = types.Integer
