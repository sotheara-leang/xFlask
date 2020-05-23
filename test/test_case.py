from flask_testing import TestCase

from test import *


class TestCase(TestCase):

    def create_app(self):
        return application.app

    def setUp(self):
        application.init()

        #db.create_all()

    def tearDown(self):
        db.session.remove()
        #db.drop_all()
