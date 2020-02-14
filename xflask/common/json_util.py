import json


def to_dict(obj):
    if isinstance(obj, str):
        return json.loads(obj)
    else:
        return json.loads(json.dumps(obj, default=lambda o: o.__dict__))

def to_json(obj):
    return json.dumps(obj.__dict__)
