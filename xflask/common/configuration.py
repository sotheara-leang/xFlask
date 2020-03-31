import yaml
from yaml import Loader

from xflask.common.util import load_config, get_file_path, merge_dict


class Configuration:

    def __init__(self, conf_file):
        self.cfg = load_config(conf_file)

    def exist(self, key):
        return True if self.get(key) is not None else False

    def get(self, key, default=None):
        value = None
        try:
            keys = key.split(':')
            if len(keys) > 1:
                value = self.__get_nest_value(self.cfg[keys[0]], keys[1:])
            else:
                value = self.cfg[key]

            if value is None and default is not None:
                value = default

        except Exception:
            pass

        return value

    def set(self, key, value):
        self.cfg.__setitem__(key, value)

    def __get_nest_value(self, map_, keys):
        if len(keys) > 1:
            return self.__get_nest_value(map_[keys[0]], keys[1:])
        else:
            return map_[keys[0]]

    def dump(self):
        return yaml.dump(self.cfg, Dumper=yaml.Dumper)

    def merge(self, conf_file):
        with open(get_file_path(conf_file), 'r') as file:
            cfg = yaml.load(file, Loader=Loader)

            merge_dict(self.cfg, cfg)
