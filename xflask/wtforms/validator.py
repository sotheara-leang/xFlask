from wtforms.validators import *


class EnumValidator(object):

    def __init__(self, enum=None, message=None):
        self.enum = enum
        self.message = message

    def __call__(self, form, field):
        if field.data is not None:
            enum = self.enum.value_of(field.data)
            if enum is None:
                if self.message is None:
                    message = field.gettext('The value is invalid')
                else:
                    message = self.message

                field.errors[:] = []
                raise StopValidation(message)
