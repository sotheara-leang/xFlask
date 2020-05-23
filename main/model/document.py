from xflask.sqlalchemy import Column, relationship
from xflask.sqlalchemy import Integer, String
from xflask.sqlalchemy.model import Model


class Document(Model):

    id          = Column(Integer, primary_key=True)
    title       = Column(String(50))

    words       = relationship('Word', secondary='document_word', lazy=True)
