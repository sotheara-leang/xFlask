import collections
import logging.config
import os

from xflask.common.util import load_config, merge_dict


class Logger(object):

    def __init__(self, conf_file):
        self.config = load_config(conf_file)

        self.init_log_dir(self.config)

        logging.config.dictConfig(self.config)

    def merge(self, conf_file):
        config = load_config(conf_file)
        merge_dict(self.config, config)

        logging.config.dictConfig(self.config)

    def init_log_dir(self, dict_):
        for k, v in dict_.items():
            if k == 'filename':
                filename = v
                file_dir = os.path.dirname(os.path.abspath(filename))

                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
            elif isinstance(v, collections.Mapping):
                self.init_log_dir(v)
