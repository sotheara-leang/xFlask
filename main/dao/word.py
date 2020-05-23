from xflask.dao import Dao

from main.model.word import Word


class WordDao(Dao):

    def __init__(self):
        super(WordDao, self).__init__(Word)

