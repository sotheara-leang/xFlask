from xflask.type.status_code import StatusCode


class Exception(Exception):

    def __init__(self, code: StatusCode):
        self.code = code
