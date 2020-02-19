import enum


class Enum(enum.Enum):

    def code(self):
        return self.value[0] if isinstance(self.value, tuple) else self.value

    def desc(self):
        return self.value[1] if isinstance(self.value, tuple) else None

    def type(self):
        return type(self.value[0])

    @classmethod
    def value_of(cls, code):
        result = None
        for e in cls:
            e_value = e.value if not isinstance(e.value, tuple) else e.value[0]
            if e_value == code:
                result = e
                break
        return result
