from xflask.wtforms import Field


class EnumField(Field):

    def __init__(self, enum, label=None, validators=None, **kwargs):
        super(EnumField, self).__init__(label, validators, **kwargs)
        self.enum = enum

    def process_formdata(self, valuelist):
        self.data = self.enum.value_of(valuelist[0])

    def _value(self):
        return self.data.code()

