from xflask.sqlalchemy import Column, ForeignKey, relationship
from xflask.sqlalchemy import Integer, String, StringEnum
from xflask.sqlalchemy.model import AuditModel

from main.type.edu_level import EducationLevel


class User(AuditModel):

    id          = Column(Integer, primary_key=True)
    username    = Column(String(50), unique=True, nullable=False)
    password    = Column(String(50), unique=False, nullable=False)
    email       = Column(String(120), unique=True, nullable=False)

    edu_level   = Column(StringEnum(EducationLevel), nullable=False)

    role_id     = Column(Integer, ForeignKey('role.id'))
    role        = relationship('Role', lazy=True)

    _hidden_columns = [
        'password'
    ]
