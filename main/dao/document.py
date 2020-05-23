from xflask.dao import Dao

from main.model.document import Document


class DocumentDao(Dao):

    def __init__(self):
        super(DocumentDao, self).__init__(Document)

