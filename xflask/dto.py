class Dto(object):

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            if isinstance(value, dict):
                value = Dto(**value)

            self.__dict__[name] = value
