from xflask.model import *
from xflask.type import StringEnum

from main.type.edu_level import EducationLevel


class User(Model, AuditableMixin):

    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(50), unique=True, nullable=False)
    password    = db.Column(db.String(50), unique=False, nullable=False)
    email       = db.Column(db.String(120), unique=True, nullable=False)

    edu_level   = db.Column(StringEnum(EducationLevel), nullable=False)

    role_id     = db.Column(db.Integer, db.ForeignKey('role.id'))

    _hidden_fields = [
        'password',
        'role'
    ]
