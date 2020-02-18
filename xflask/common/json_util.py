import json
import enum

from xflask.type import Enum as Enum


def to_dict(obj, serialize_enum=False):
    if isinstance(obj, Enum):
        return obj.code() if serialize_enum is True else obj

    if isinstance(obj, enum.Enum):
        return obj.value if serialize_enum is True else obj

    if not hasattr(obj, "__dict__"):
        return obj

    result = {}
    for key, val in obj.__dict__.items():
        if key.startswith("_"):
            continue

        element = []
        if isinstance(val, list):
            for item in val:
                element.append(to_dict(item, serialize_enum))
        else:
            element = to_dict(val, serialize_enum)

        result[key] = element

    return result

def serialize(obj):
    return to_dict(obj, True)

def to_json(obj):
    return json.dumps(serialize(obj))


if __name__ == '__main__':
    pass
