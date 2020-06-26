import glob
import re
import sys

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


def scan_namespaces(package):
    namespaces = []

    file_path = os.path.join(get_root_dir(), package.replace('.', '/')) + '.py'
    if is_file(file_path):
        # file
        namespaces.append(package)
    else:
        # directory
        files_pattern = os.path.join(get_root_dir(), package.replace('.', '/'), '**/*.py')
        for file in glob.glob(files_pattern, recursive=True):
            file_name = os.path.basename(file)
            if file_name.startswith('_') or 'migrate' in file_name or 'server' in file_name:
                continue

            namespace = file.replace(get_root_dir(), '')
            namespace = re.sub('/+', '.', namespace)
            namespace = namespace[1:-3]
            namespaces.append(namespace)

    return namespaces


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
