from xflask.common.file_util import *
from xflask.common.json_util import *

from flask import current_app

def get_xflask():
    try:
        return current_app.extensions['xflask']
    except KeyError:
        raise RuntimeError("You must initialize xflask before using this method")
