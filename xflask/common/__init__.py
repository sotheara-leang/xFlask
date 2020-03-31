import sys
from flask import current_app


def get_xflask():
    return get_extension('xflask')

def get_extension(extension):
    try:
        return current_app.extensions.get(extension)
    except KeyError:
        raise RuntimeError("You must initialize xflask before using this method")

def exit(code=None):
    def function(f):
        def wrapper(*args, **kwargs):
            try:
                result = f(*args, **kwargs)
            except Exception:
                sys.exit(code)
            return result
        return wrapper
    return function
