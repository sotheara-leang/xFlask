import importlib
import json
import os


def get(obj, default):
    return obj if obj is not None else default


def to_dict(obj):
    if isinstance(obj, str):
        return json.loads(obj)
    else:
        return json.loads(json.dumps(obj, default=lambda o: o.__dict__))


def to_json(obj):
    return json.dumps(obj.__dict__)


def import_modules(root_dir, model_pkgs):
    for model_pkg in model_pkgs:
        for module in os.listdir(root_dir + '/' + model_pkg.replace('.', '/')):
            if module == '__init__.py' or module[-3:] != '.py':
                continue

            model_namespace = model_pkg + '.' + module[:-3]

            importlib.import_module(model_namespace)
