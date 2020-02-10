from xflask import db
from xflask.model import Model


class User(Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    _default_fields = [
        "username",
        "email",
    ]

    _hidden_fields = [
        "password",
    ]

    _readonly_fields = [

    ]
