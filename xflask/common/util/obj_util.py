import collections


def get_attr(obj, attr_name):
    return obj[attr_name] if isinstance(obj, dict) else getattr(obj, attr_name)


def to_dict(obj):
    if not hasattr(obj, '__dict__'):
        return obj

    if hasattr(obj, 'to_dict'):
        return obj.to_dict()

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


#### DICT ####

def merge_dict(obj_dict: dict, merge_dct: dict):
    for k, v in iter(merge_dct.items()):
        if k in obj_dict and isinstance(obj_dict[k], dict) and isinstance(merge_dct[k], dict):
            merge_dict(obj_dict[k], merge_dct[k])
        else:
            obj_dict[k] = merge_dct[k]


def update_dict(obj_dict, key, value):
    _key = key.split(':')[0]
    _next_key = ''.join(key.split(':')[1:])

    for k, v in obj_dict.items():
        if k == _key:
            if isinstance(v, collections.Mapping):
                update_dict(v, _next_key, value)
            else:
                if type(value) == type(v):
                    obj_dict[_key] = value
