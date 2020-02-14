from xflask.type import Enum


class BizCode(Enum):

    USER_NOT_FOUND     = '10100', 'User not found'
    PWD_INVALID        = '10101', 'Password invalid'
