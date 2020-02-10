from flask_testing import TestCase

from test import *


class TestCase(TestCase):

    def create_app(self):
        return server.app

    def setUp(self):
        server.init()
        self.injector = server.flask_injector.injector
        self.client = server.app.test_client()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
