from xflask.marshmallow import Str, validate
from xflask.marshmallow.schema import Schema


class LoginVo(Schema):

    username: Str(validate=validate.Length(min=2, max=50), required=True)
    password: Str(validate=validate.Length(min=2, max=50), required=True)




