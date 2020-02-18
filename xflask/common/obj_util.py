import json
import enum

from xflask.type import Enum as Enum


def to_dict(obj, serialize=False):
    if isinstance(obj, Enum):
        return obj.code() if serialize is True else obj

    if isinstance(obj, enum.Enum):
        return obj.value if serialize is True else obj

    if not hasattr(obj, "__dict__"):
        return obj

    result = {}
    for key, val in obj.__dict__.items():
        if key.startswith("_"):
            continue

        element = []
        if isinstance(val, list):
            for item in val:
                element.append(to_dict(item, serialize))
        else:
            element = to_dict(val, serialize)

        result[key] = element

    return result

def serialize(obj):
    return to_dict(obj, True)

def to_json(obj, **kwargs):
    return json.dumps(serialize(obj), kwargs)


if __name__ == '__main__':
    pass
