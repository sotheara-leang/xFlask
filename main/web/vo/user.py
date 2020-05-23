from xflask.marshmallow import Int, Str, Enum, Email, validate
from xflask.marshmallow.schema import Schema

from main.type.edu_level import EducationLevel


class UserVo(Schema):

    id          : Int(required=True)
    username    : Str(validate=validate.Length(min=2, max=50), required=True)
    password    : Str(validate=validate.Length(min=2, max=50), required=True)
    email       : Email(required=True)
    edu_level   : Enum(EducationLevel, required=True)
    role_id     : Int(required=True)
