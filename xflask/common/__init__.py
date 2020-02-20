from xflask.common.file_util import *
from xflask.common.obj_util import *

from flask import current_app


def get_xflask():
    return get_extension('xflask')

def get_extension(extension):
    try:
        return current_app.extensions.get(extension)
    except KeyError:
        raise RuntimeError("You must initialize xflask before using this method")
