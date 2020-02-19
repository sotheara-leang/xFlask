from datetime import datetime
from xflask.type.enum import Enum
from xflask.common.date_util import dd_MM_yyyy_hh_mm_ss, to_date_str


class Serializer(object):

    def accept(self, obj):
        pass

    def serialize(self, obj):
        pass


class EnumSerializer(Serializer):

    def accept(self, obj):
        return isinstance(obj, Enum)

    def serialize(self, obj):
        return obj.code()


class DateTimeSerializer(Serializer):

    def accept(self, obj):
        return isinstance(obj, datetime)

    def serialize(self, obj):
        return to_date_str(obj, dd_MM_yyyy_hh_mm_ss)
