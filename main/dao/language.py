from xflask.dao import Dao

from main.model.language import Language


class LanguageDao(Dao):

    def __init__(self):
        super(LanguageDao, self).__init__(Language)

