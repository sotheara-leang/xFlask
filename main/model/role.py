from xflask import db
from xflask.model import Model


class Role(Model):

    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String(50), unique=False, nullable=False)

    users   = db.relationship('User', backref='role', lazy=True)
