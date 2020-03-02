class Param(object):
    def __init__(self, name=None):
        self.name = name


class Header(object):

    def __init__(self, name=None):
        self.name = name


class Body(object):

    def __init__(self, type=None, exclude=[]):
        self.type = type
        self.exclude = exclude


class JsonBody(object):

    def __init__(self, type=None, exclude=[]):
        self.type = type
        self.exclude = exclude


class FormBody(object):

    def __init__(self, type=None, exclude=[]):
        self.type = type
        self.exclude = exclude



