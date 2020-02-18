from xflask import db


def transactional(subtransactions=True, nested=False):
    def function(f):
        def wrapper(*args, **kwargs):
            db.session.begin(subtransactions=subtransactions, nested=nested)
            try:
                result = f(*args, **kwargs)
            except Exception as e:
                db.session.rollback()
                raise e
            db.session.commit()
            return result
        return wrapper
    return function
