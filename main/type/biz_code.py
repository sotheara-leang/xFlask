from xflask.type import Enum


class BizCode(Enum):
    USER_NAME_EXISTED       = '10100', 'Username Existed'
    USER_PWD_INVALID        = '10101', 'Password Invalid'
