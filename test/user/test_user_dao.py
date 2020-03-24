from test.test_case import TestCase
from main.dao.user import UserDao
from main.model.user import User
from main.type.edu_level import EducationLevel


class TestUserDao(TestCase):

    def setUp(self):
        super().setUp()

        self.user_dao = self.injector.get(UserDao)

    def test_create(self):
        user = User(username='user1', password='123',
                    email='user1@example.com', edu_level=EducationLevel.BACHELOR)

        self.user_dao.insert(user)

    def test_create_with_dict(self):
        user = {'username': 'user2', 'password': '123', 'email': 'user2@gmail.com',
                'edu_level': EducationLevel.BACHELOR}

        self.user_dao.insert(user)

    def test_get(self):
        user = self.user_dao.get(43)
        print('\n', user)

    def test_get_all(self):
        users = self.user_dao.get_all()
        print('\n', users)

    def test_get_by_username(self):
        user = self.user_dao.get_by_username(username='user1')
        print('\n', user)

    def test_update(self):
        user = self.user_dao.get(50)
        user.email = 'new@email.com'

        self.user_dao.update(user)

    def test_update_with_dict(self):
        user = {'id': 51, 'username': 'user3', 'email': 'user3@gmail.com'}

        self.user_dao.update(user)

    def test_delete(self):
        self.user_dao.delete(43)

    def test_merge(self):
        user = {'id': 51, 'username': 'user2', 'email': 'user2@gmail.com'}

        user = self.user_dao.merge(user)

        print(user)
