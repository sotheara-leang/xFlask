from xflask.type.status_code import StatusCode


class BizCode(StatusCode):
    ...

# status code

BC_USER_NOT_FOUND     = BizCode('1100', 'user not found')
BC_PWD_INVALID        = BizCode('1101', 'password invalid')


