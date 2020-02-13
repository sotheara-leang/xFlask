import importlib
import json
import os
import sys

from flask import current_app

def get_xflask():
    try:
        return current_app.extensions['xflask']
    except KeyError:
        raise RuntimeError("You must initialize xflask before using this method")

def setup_root_dir(root_dir_name):
    cur_dir = os.getcwd()
    while True:
        if os.path.basename(cur_dir) == root_dir_name:
            root_dir = cur_dir
            break
        else:
            cur_dir = os.path.dirname(cur_dir)

    os.environ['PROJ_HOME'] = root_dir
    sys.path.append(root_dir)

def import_modules(root_dir, model_pkgs):
    for model_pkg in model_pkgs:
        for module in os.listdir(root_dir + '/' + model_pkg.replace('.', '/')):
            if module == '__init__.py' or module[-3:] != '.py':
                continue

            model_namespace = model_pkg + '.' + module[:-3]

            importlib.import_module(model_namespace)

def get_root_dir():
    return os.environ['PROJ_HOME']

def get_file(file):
    return os.path.join(get_root_dir(), file)

def to_dict(obj):
    if isinstance(obj, str):
        return json.loads(obj)
    else:
        return json.loads(json.dumps(obj, default=lambda o: o.__dict__))

def to_json(obj):
    return json.dumps(obj.__dict__)
