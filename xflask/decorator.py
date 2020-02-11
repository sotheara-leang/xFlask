from functools import wraps

from xflask import db


def transactional(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        f(*args, **kwargs)
        db.session.commit()

    return wrap
