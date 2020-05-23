from xflask.sqlalchemy import session, transactional

from test.test_case import *

from main.dao.document import DocumentDao
from main.dao.word import WordDao
from main.dao.document_word import DocumentWordDao

from main.model.document import Document
from main.model.word import Word
from main.model.document_word import DocumentWord


class TestDocument(TestCase):

    def setUp(self):
        super().setUp()

        self.doc_dao = application.get_component(DocumentDao)
        self.word_dao = application.get_component(WordDao)
        self.doc_word_dao = application.get_component(DocumentWordDao)

    def test_create_doc(self):
        word1 = Word(word='hello')
        # self.word_dao.insert(word1)  # no need to insert

        doc1 = Document(title='doc1')
        # self.doc_dao.insert(doc1)    # no need to insert

        doc_word1 = DocumentWord(document=doc1, word=word1)
        self.doc_word_dao.insert(doc_word1)

    def test_create_doc_2(self):
        word1 = Word(word='hello')

        doc1 = Document(title='doc1')
        doc1.words.append(word1)

        self.doc_dao.insert(doc1)

    @transactional()
    def test_insert_word_to_doc(self):
        word = self.word_dao.get(1)
        doc = self.doc_dao.get(1)

        doc.words.append(word)

    def test_delete_word_from_doc(self):
        doc = self.doc_dao.get(1)

        session.begin()

        for word in doc.words:
            if word.word == 'hello':
                doc.words.remove(word)

        session.commit()

    def test_get_word(self):
        word = self.word_dao.get(1)

        print(word)
