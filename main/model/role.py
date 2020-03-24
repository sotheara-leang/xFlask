from xflask.sqlalchemy import Column, relationship
from xflask.sqlalchemy import Integer, String
from xflask.sqlalchemy.model import AuditModel


class Role(AuditModel):

    id      = Column(Integer, primary_key=True)
    name    = Column(String(50), unique=False, nullable=False)
    users   = relationship('User', backref='role', lazy=True)
