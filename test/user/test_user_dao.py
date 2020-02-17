from test.test_case import *

from main.model.user import User
from main.model.role import Role

from main.dao.user import UserDao
from main.dao.role import RoleDao
from main.type.edu_level import EducationLevel


class TestUserDao(TestCase):

    def setUp(self):
        super().setUp()

        self.user_dao = self.injector.get(UserDao)

    def test_create(self):
        user = User(username='user1', password='123',
                    email='user1@example.com', edu_level=EducationLevel.BACHELOR)

        self.user_dao.insert(user)

    def test_get_by_id(self):
        user = self.user_dao.get(43)
        print('\n', user)

    def test_get_all(self):
        users = self.user_dao.get_all()
        print('\n', users)

    def test_get_by_username(self):
        user = self.user_dao.get_by_username(username='user1')
        print('\n', user)

    def test_update(self):
        user = self.user_dao.get_by_id(49)
        user.email = 'new@email.com'

        self.user_dao.update(user)

    def test_delete_by_id(self):
        self.user_dao.delete_by_id(43)


