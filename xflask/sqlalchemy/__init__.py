from sqlalchemy import *
from sqlalchemy.orm import *
from flask_sqlalchemy import SQLAlchemy

from .decorator import *
from .util import *


db = SQLAlchemy(session_options={'autocommit': True})

session = db.session


def transactional(subtransactions=True, nested=False):
    def function(f):
        def wrapper(*args, **kwargs):
            db.session.begin(subtransactions=subtransactions, nested=nested)
            try:
                result = f(*args, **kwargs)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

            return result

        return wrapper

    return function
