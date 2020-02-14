from xflask.type import Enum


class Exception(Exception):

    def __init__(self, code: Enum):
        self.code = code
