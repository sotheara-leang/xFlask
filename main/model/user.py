from xflask.model import *


class User(Model):

    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(50), unique=True, nullable=False)
    password    = db.Column(db.String(50), unique=False, nullable=False)
    email       = db.Column(db.String(120), unique=True, nullable=False)

    role_id     = db.Column(db.Integer, db.ForeignKey('role.id'))

    _hidden_fields = [
        'password',
        'role'
    ]
