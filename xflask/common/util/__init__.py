import sys
import importlib
import re
import yaml

from xflask.common.util.file_util import *
from xflask.common.util.obj_util import *


def setup_env(root_dir_name):
    cur_dir = os.getcwd()
    while True:
        if os.path.basename(cur_dir) == root_dir_name:
            root_dir = cur_dir
            break
        else:
            cur_dir = os.path.dirname(cur_dir)

    os.environ['PROJ_HOME'] = root_dir
    os.environ['XFLASK_HOME'] = os.path.dirname(xflask.__file__)

    sys.path.append(root_dir)

def import_modules(root_dir, model_pkgs):
    for model_pkg in model_pkgs:
        for module in os.listdir(root_dir + '/' + model_pkg.replace('.', '/')):
            if module == '__init__.py' or module[-3:] != '.py':
                continue

            model_namespace = model_pkg + '.' + module[:-3]

            importlib.import_module(model_namespace)

def load_config(conf_file):
    with open(conf_file, 'r') as f:
        param_matcher = re.compile(r'.*\$\{([^}^{]+)\}.*')

        def param_constructor(loader, node):
            value = node.value

            params = param_matcher.findall(value)
            for param in params:
                try:
                    param_value = os.environ[param]
                    return value.replace('${' + param + '}', param_value)
                except Exception:
                    pass

            return value

        class VariableLoader(yaml.SafeLoader):
            pass

        VariableLoader.add_implicit_resolver('!param', param_matcher, None)
        VariableLoader.add_constructor('!param', param_constructor)

        config = yaml.load(f.read(), Loader=VariableLoader)

        return config
