from xflask.common import to_dict
from xflask.type import Enum
from xflask.type.status_code import StatusCode


class Response(object):

    def __init__(self, code: Enum, data=None):
        self.status = code.code()
        self.message = code.desc()
        self.data = data

    def to_dict(self):
        return to_dict(self)

    @classmethod
    def success(cls, data=None):
        return Response(StatusCode.SUCCESS, data)

    @classmethod
    def fail(cls, code=None, data=None):
        if code is not None:
            return Response(code, data)
        else:
            return Response(StatusCode.SYS_ERROR, data)

    @classmethod
    def not_found(cls):
        return Response(StatusCode.NOT_FOUND)

    @classmethod
    def existed(cls):
        return Response(StatusCode.EXISTED)
