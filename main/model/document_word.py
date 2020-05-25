from xflask.sqlalchemy import Column, ForeignKey, relationship
from xflask.sqlalchemy import Integer
from xflask.sqlalchemy.model import Model


class DocumentWord(Model):

    document_id     = Column(Integer, ForeignKey('document.id'), primary_key=True)
    word_id         = Column(Integer, ForeignKey('word.id'), primary_key=True)

    document        = relationship('Document', lazy=True)   # to reference to parent
    word            = relationship('Word', lazy=True)       # to reference to child
