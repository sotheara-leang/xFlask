from marshmallow import fields, validate

from xflask.web.vo import Vo


class LoginVo(Vo):

    username: fields.Str(validate=validate.Length(min=2, max=50), required=True)
    password: fields.Str(validate=validate.Length(min=2, max=50), required=True)




