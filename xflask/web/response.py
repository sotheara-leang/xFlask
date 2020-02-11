from xflask.common.util import to_dict
from xflask.type.status_code import *


class Response(object):

    def __init__(self, status, message, data=None):
        self.status = status
        self.message = message
        self.data = data

    def to_dict(self):
        return to_dict(self)

    @classmethod
    def success(cls, data=None):
        return Response(SC_SUCCESS.code, SC_SUCCESS.msg, data)

    @classmethod
    def fail(cls, data=None):
        if isinstance(data, StatusCode):
            return Response(data.code, data.msg)
        else:
            return Response(SC_SYS_ERROR.code, SC_SYS_ERROR.msg, data)

    @classmethod
    def fail_with_custom_code(cls, code=None, data=None):
        return Response(code.code, code.msg, data)

    @classmethod
    def invalid(cls, data=None):
        return Response(SC_INVALID.code, SC_INVALID.msg, data)
