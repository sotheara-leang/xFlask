from xflask.sqlalchemy import Column, relationship
from xflask.sqlalchemy import Integer, String
from xflask.sqlalchemy.model import Model


class Word(Model):

    id          = Column(Integer, primary_key=True)
    word        = Column(String(50))

    docs        = relationship('Document', secondary='document_word', lazy=True)
