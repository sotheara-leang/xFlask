from xflask.type import Enum
from xflask.type.sys_code import SysCode


class Response(object):

    def __init__(self, code: Enum, data=None):
        self.status = code.code()
        self.message = code.desc()
        self.data = data

    @classmethod
    def success(cls, data=None):
        return Response(SysCode.SUCCESS, data)

    @classmethod
    def fail(cls, code=None, data=None):
        if code is not None:
            return Response(code, data)
        else:
            return Response(SysCode.SYS_ERROR, data)

    @classmethod
    def not_found(cls):
        return Response(SysCode.NOT_FOUND)

    @classmethod
    def existed(cls):
        return Response(SysCode.EXISTED)

    @classmethod
    def invalid(cls, data=None):
        return Response(SysCode.INVALID, data)
