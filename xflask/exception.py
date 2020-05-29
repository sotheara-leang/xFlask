from xflask.type import Enum
from xflask.type import SysCode


class Exception(Exception):

    def __init__(self, code: Enum = SysCode.SYS_ERROR, data=None):
        self.code = code
        self.data = data
