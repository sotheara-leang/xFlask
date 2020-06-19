class UrlParam(object):
    def __init__(self, name=None, default=None, required=True, type=None, list=False):
        self.name = name
        self.default = default
        self.required = required
        self.type = type
        self.list = list

class Header(object):

    def __init__(self, name=None, default=None, required=True):
        self.name = name
        self.default = default
        self.required = required
