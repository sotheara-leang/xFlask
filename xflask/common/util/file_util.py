import os
import xflask


def get_root_dir():
    return os.environ['PROJ_HOME']

def path_exist(path):
    return os.path.exists(path)

def is_dir(path):
    return os.path.isdir(path)

def is_file(path):
    return os.path.isfile(path)

def get_dir_path(path):
    return os.path.dirname(path)

def get_dir_name(path):
    return get_file_name(get_dir_path(path))

def get_file_path(file):
    return os.path.join(get_root_dir(), file)

def get_file_name(path):
    return os.path.basename(path)

def get_xflask_path(path=None):
    xflask_dir = get_dir_path(xflask.__file__)
    return os.path.join(xflask_dir, path)
