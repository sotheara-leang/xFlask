from marshmallow import Schema, fields, validate

from xflask.web.vo import *


class CreateUserVo(Vo):

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    @classmethod
    def schema(cls):
        return Schema.from_dict({
            'username': fields.Str(validate=validate.Length(min=2, max=50), required=True),
            'password': fields.Str(validate=validate.Length(min=2, max=50), required=True)
        })()



