from marshmallow import fields, validate

from xflask.marshmallow import field
from xflask.web.vo import Vo

from main.type.edu_level import EducationLevel


class UserVo(Vo):

    id          : fields.Int(required=True)
    username    : fields.Str(validate=validate.Length(min=2, max=50), required=True)
    password    : fields.Str(validate=validate.Length(min=2, max=50), required=True)
    email       : fields.Email(required=True)
    edu_level   : field.Enum(EducationLevel, required=True)
    role_id     : fields.Int(required=True)
