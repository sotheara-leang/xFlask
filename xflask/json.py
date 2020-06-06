from datetime import datetime
import decimal

from xflask.sqlalchemy.model import Model
from xflask.type.enum import Enum


class JsonSerializer(object):

    def check(self, obj):
        return False

    def serialize(self, obj):
        return None


class EnumSerializer(JsonSerializer):

    def check(self, obj):
        return isinstance(obj, Enum)

    def serialize(self, obj):
        return obj.code()


class DateTimeSerializer(JsonSerializer):

    def __init__(self, fmt='%d-%m-%Y %H:%M:%S'):
        self.fmt = fmt

    def check(self, obj):
        return isinstance(obj, datetime)

    def serialize(self, obj):
        return obj.strftime(self.fmt)


class DecimalSerializer(JsonSerializer):

    def check(self, obj):
        return isinstance(obj, decimal.Decimal)

    def serialize(self, obj):
        decimal_as_str = str(obj)
        return float(decimal_as_str)


class ModelSerializer(JsonSerializer):

    def check(self, obj):
        return isinstance(obj, Model)

    def serialize(self, obj):
        return obj.to_dict()


JSON_SERIALIZERS = [
    EnumSerializer(),
    DateTimeSerializer(),
    DecimalSerializer(),
    ModelSerializer()
]
