import os
import sys

from flask_sqlalchemy import SQLAlchemy

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


db = SQLAlchemy()

