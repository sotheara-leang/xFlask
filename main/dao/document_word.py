from xflask.dao import Dao

from main.model.document_word import DocumentWord


class DocumentWordDao(Dao):

    def __init__(self):
        super(DocumentWordDao, self).__init__(DocumentWord)

