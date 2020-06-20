from xflask.sqlalchemy import Column
from xflask.sqlalchemy import Integer, String
from xflask.sqlalchemy.model import SoftModel


class Language(SoftModel):

    id          = Column(Integer, primary_key=True)
    name        = Column(String(150), unique=True, nullable=True)
    description = Column(String(225), unique=False, nullable=True)


