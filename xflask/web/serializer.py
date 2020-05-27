from datetime import datetime

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


class ModelSerializer(JsonSerializer):

    def check(self, obj):
        return isinstance(obj, Model)

    def serialize(self, obj):
        return obj.to_dict()
