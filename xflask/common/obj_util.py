import enum
from datetime import datetime
from xflask.common.date_util import to_date_str
from xflask.type import Enum as Enum


def get_attr(obj, attr_name):
    return obj[attr_name] if isinstance(obj, dict) else getattr(obj, attr_name)

def to_dict(obj):
    if not hasattr(obj, '__dict__'):
        return obj

    result = {}
    for key, val in obj.__dict__.items():
        if key.startswith("_"):
            continue

        element = []
        if isinstance(val, list):
            for item in val:
                element.append(to_dict(item))
        else:
            element = to_dict(val)

        result[key] = element

    return result

def serialize(obj, show=[], hidden=[], dept=0):
    if not hasattr(obj, '__dict__'):
        # primitive type
        if isinstance(obj, Enum):
            return obj.code()
        elif isinstance(obj, enum.Enum):
            return obj.value
        elif isinstance(obj, datetime):
            return to_date_str(obj)
        else:
            return obj

    if hasattr(obj, '_hidden'):
        _hidden = getattr(obj, '_hidden')
        hidden.extend(_hidden)
    if hasattr(obj, '_show'):
        _show = getattr(obj, '_show')
        show.extend(_show)

    hidden = [e for e in hidden if e not in show]

    if hasattr(obj, 'serialize'):
        return obj.serialize(show, hidden)

    result = {}
    for key, val in obj.__dict__.items():
        if key.startswith("_") or key in hidden:
            continue

        element = []
        if isinstance(val, list):
            if dept > 0:
                item_show = [e.split('.')[1] for e in show if e.split('.')[0] == key]
                item_hidden = [e.split('.')[1] for e in hidden if e.split('.')[0] == key]
            else:
                item_show = show
                item_hidden = hidden

            for item in val:
                element.append(serialize(item, item_show, item_hidden, dept + 1))

        elif hasattr(val, 'serialize'):
            if dept > 0:
                item_show = [e.split('.')[1] for e in show if e.split('.')[0] == key]
                item_hidden = [e.split('.')[1] for e in hidden if e.split('.')[0] == key]
            else:
                item_show = show
                item_hidden = hidden

            element = serialize(val, item_show, item_hidden, dept + 1)
        else:
            element = serialize(val, dept=dept + 1)

        result[key] = element

    return result
