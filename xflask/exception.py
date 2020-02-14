from xflask.type import Type


class Exception(Exception):

    def __init__(self, code: Type):
        self.code = code
