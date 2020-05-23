from main.service.user import UserService
from test.test_case import *


class TestServiceUser(TestCase):

    def setUp(self):
        super().setUp()

        self.user_service = application.get_component(UserService)

    def test_get(self):
        user = self.user_service.get(43)
        print('\n',  user)

    def test_get_by_username(self):
        user = self.user_service.get_by_username('user1')
        print('\n', user)


