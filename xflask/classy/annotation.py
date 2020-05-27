class Param(object):
    def __init__(self, name=None, required=True):
        self.name = name
        self.required = required


class Header(object):

    def __init__(self, name=None, required=True):
        self.name = name
        self.required = required
