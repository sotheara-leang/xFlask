class Param(object):
    def __init__(self, name=None, required=True):
        self.name = name
        self.required = required


class Header(object):

    def __init__(self, name=None, required=True):
        self.name = name
        self.required = required


## JSON ##

class JsonBody(object):

    def __init__(self, type=None, exclude=[]):
        self.type = type
        self.exclude = exclude


class JsonField(object):

    def __init__(self, name, required=True):
        self.name = name
        self.required = required


## FORM ##

class FormBody(object):

    def __init__(self, type=None, exclude=[]):
        self.type = type
        self.exclude = exclude


class FormField(object):

    def __init__(self, name, required=True):
        self.name = name
        self.required = required


