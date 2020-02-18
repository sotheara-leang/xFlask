from marshmallow import fields, validate

from xflask.web.vo import *
from xflask.marshmallow import field

from main.type.edu_level import EducationLevel


class CreateUserVo(Vo):

    def __init__(self, username=None, password=None, email=None, edu_level=None, role_id=None):
        self.username = username
        self.password = password
        self.email = email
        self.edu_level = edu_level
        self.role_id = role_id

    @classmethod
    def schema(cls):
        return {
            'username': fields.Str(validate=validate.Length(min=2, max=50), required=True),
            'password': fields.Str(validate=validate.Length(min=2, max=50), required=True),
            'email': fields.Email(required=True),
            'edu_level': field.Enum(EducationLevel, required=True),
            'role_id': fields.Int(required=True)
        }
