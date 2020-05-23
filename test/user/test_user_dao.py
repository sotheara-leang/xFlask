from test.test_case import *
from main.dao.user import UserDao
from main.model.user import User
from main.type.edu_level import EducationLevel


class TestUserDao(TestCase):

    def setUp(self):
        super().setUp()

        self.user_dao = application.get_component(UserDao)

    def test_exist(self):
        self.user_dao.exist(9)

    def test_create(self):
        user = User(username='user1', password='123',
                    email='user1@example.com', edu_level=EducationLevel.BACHELOR)

        self.user_dao.insert(user)

    def test_create_with_dict(self):
        user = {'username': 'user2', 'password': '123', 'email': 'user2@gmail.com',
                'edu_level': EducationLevel.BACHELOR}

        self.user_dao.insert(user)

    def test_get(self):
        user = self.user_dao.get(9)
        print('\n', user)

    def test_get_all(self):
        users = self.user_dao.get_all()
        print('\n', users)

    def test_get_by_username(self):
        user = self.user_dao.get_by_username(username='user1')
        print('\n', user)

    def test_update(self):
        user = self.user_dao.get(8)
        user.email = 'new@email.com'

        self.user_dao.update(user)

    def test_update_by_dict(self):
        user = {'id': 8, 'email': 'user31@gmail.com'}

        self.user_dao.update(user)

    def test_update_by_criterion(self):
        user = {'email': 'user31@gmail.com'}

        self.user_dao.update(user, id=9)

    def test_delete_by_id(self):
        self.user_dao.delete(4)

    def test_delete_by_obj(self):
        self.user_dao.delete(self.user_dao.get(5))

    def test_delete_by_criterion(self):
        self.user_dao.delete(username='user2')

    def test_merge(self):
        user = {'id': 51, 'username': 'user2', 'email': 'user2@gmail.com'}

        user = self.user_dao.merge(user)

        print(user)
