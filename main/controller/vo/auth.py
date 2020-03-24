from xflask.marshmallow import Str
from xflask.marshmallow import validate

from xflask.web.vo import Vo


class LoginVo(Vo):

    username: Str(validate=validate.Length(min=2, max=50), required=True)
    password: Str(validate=validate.Length(min=2, max=50), required=True)




