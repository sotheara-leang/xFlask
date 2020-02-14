import os
import sys
import importlib


def get_root_dir():
    return os.environ['PROJ_HOME']

def get_file(file):
    return os.path.join(get_root_dir(), file)

def import_modules(root_dir, model_pkgs):
    for model_pkg in model_pkgs:
        for module in os.listdir(root_dir + '/' + model_pkg.replace('.', '/')):
            if module == '__init__.py' or module[-3:] != '.py':
                continue

            model_namespace = model_pkg + '.' + module[:-3]

            importlib.import_module(model_namespace)

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
