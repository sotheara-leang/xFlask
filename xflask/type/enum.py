import enum


class Enum(enum.Enum):

    def code(self):
        return self.value[0] if isinstance(self.value, tuple) else self.value

    def desc(self):
        return self.value[1] if isinstance(self.value, tuple) else None

    @classmethod
    def type(cls):
        for e in cls:
            return type(e.code())
        return None

    @classmethod
    def values(cls):
        enums = []
        for e in cls:
            enums.append(e)
        return enums

    @classmethod
    def value_of(cls, code):
        enum_type = cls.type()
        try:
            code = enum_type(code) if enum_type is not None else code
        except ValueError:
            return None

        result = None
        for e in cls:
            e_value = e.value if not isinstance(e.value, tuple) else e.value[0]
            if e_value == code:
                result = e
                break
        return result
