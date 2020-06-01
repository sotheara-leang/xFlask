from xflask.wtforms import Field
from xflask.wtforms import ValidationError

class EnumField(Field):

    def __init__(self, enum, label=None, validators=None, **kwargs):
        super(EnumField, self).__init__(label, validators, **kwargs)
        self.enum = enum

    def process_formdata(self, value_list):
        if value_list is None or len(value_list) == 0:
            return None

        self.data = self.enum.value_of(value_list[0])
        if self.data is None:
            raise ValidationError('This field is invalid')

    def _value(self):
        return self.data.code() if self.data is not None else None

