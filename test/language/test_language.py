from test.test_case import *

from main.dao.language import LanguageDao

from main.model.language import Language

class TestLanguage(TestCase):

    def setUp(self):
        super().setUp()

        self.lang_dao = application.get_component(LanguageDao)

    def test_create_lang(self):
        lang = Language(name='Khmer', description='Khmer Language')
        lang.set_soft_columns()

        self.lang_dao.insert(lang)

    def test_query_soft(self):
        langs = self.lang_dao.get_all_by_filter(soft=True)
        print(langs)
