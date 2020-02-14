from xflask.type import Type
import sqlalchemy.types as types


class StringTypeEnum(types.TypeDecorator):

    impl = types.String

    def __init__(self, enum_type: Type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enum_type = enum_type

    def process_bind_param(self, value, dialect):
        return value.code()

    def process_result_value(self, value, dialect):
        return self.enum_type.value_of(value)


class IntegerTypeEnum(StringTypeEnum):

    impl = types.Integer
