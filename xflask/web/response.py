from xflask.common import to_dict
from xflask.type import Enum
from xflask.type.sys_code import SysCode


class Response(object):

    def __init__(self, code: Enum, data=None, show=[], hidden=[]):
        self.status = code.code()
        self.message = code.desc()
        self.data = data

        # for serialization
        self._show = show
        self._hidden = hidden

    def to_dict(self):
        return to_dict(self)

    @classmethod
    def success(cls, data=None, show=[], hidden=[]):
        return Response(SysCode.SUCCESS, data, show, hidden)

    @classmethod
    def fail(cls, code=None, data=None, show=[], hidden=[]):
        if code is not None:
            return Response(code, data, show, hidden)
        else:
            return Response(SysCode.SYS_ERROR, data, show, hidden)

    @classmethod
    def not_found(cls):
        return Response(SysCode.NOT_FOUND)

    @classmethod
    def existed(cls):
        return Response(SysCode.EXISTED)
