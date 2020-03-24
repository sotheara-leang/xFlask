from xflask.marshmallow import Int, Str, Enum, Email
from xflask.marshmallow import validate
from xflask.web.vo import Vo

from main.type.edu_level import EducationLevel


class UserVo(Vo):

    id          : Int(required=True)
    username    : Str(validate=validate.Length(min=2, max=50), required=True)
    password    : Str(validate=validate.Length(min=2, max=50), required=True)
    email       : Email(required=True)
    edu_level   : Enum(EducationLevel, required=True)
    role_id     : Int(required=True)
