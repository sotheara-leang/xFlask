from xflask.common.util import to_dict


class Dto(object):

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            if isinstance(value, dict):
                value = Dto(**value)

            self.__dict__[name] = value

    def get_dict(self):
        return to_dict(self)
