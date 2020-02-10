from main.model.user import User
from main.service.user import UserService
from test.test_case import *


class TestServiceUser(TestCase):

    def test_get_user(self):
        user_service = self.injector.get(UserService)

        user = user_service.get_user(123)
        self.assertIsNone(user)

    def test_create_user(self):
        user_service = self.injector.get(UserService)

        user = User(username='user1', email='user1@gmail.com', password='123')

        user_service.create_user(user)

        new_user = user_service.get_user_by_username('user1')

        self.assertIs(user, new_user)

