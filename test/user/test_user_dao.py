from main.dao.user import UserDao
from main.model.user import User
from main.type.edu_level import EducationLevel
from test.test_case import *


class TestUserDao(TestCase):

    def setUp(self):
        super().setUp()

        self.user_dao = application.get_component(UserDao)

    def test_count(self):
        count = self.user_dao.count(username='user2')
        print(count)

    def test_exist(self):
        self.user_dao.exist(9)

    def test_create(self):
        user = User(username='user3', password='123', role_id=1,
                    email='user1@example.com', edu_level=EducationLevel.BACHELOR)

        self.user_dao.insert(user)

    def test_create_with_dict(self):
        user = {'username': 'user2', 'password': '123', 'email': 'user2@gmail.com',
                'edu_level': EducationLevel.BACHELOR}

        self.user_dao.insert(user)

    def test_get(self):
        user = self.user_dao.get(72)

        role = user.role

        dict_ = user.to_dict()

        user2 = User()

        user2.from_dict(**dict_)

        print(user2)

    def test_get_all(self):
        users = self.user_dao.get_all()
        print('\n', users)

    def test_creates_user(self):
        for i in range(50):
            username = 'user%s' % i
            edu_level = EducationLevel.BACHELOR if i % 2 == 0 else EducationLevel.MASTER
            email = 'user%s@example.com' % i

            user = User(username=username, password='', email=email, edu_level=edu_level, role_id=1)

            self.user_dao.insert(user)

    def test_get_page(self):
        pagination = self.user_dao.get_page(1, per_page=20, order=(User.id.asc(),), edu_level=EducationLevel.MASTER)

        print(pagination)

    def test_get_by_username(self):
        user = self.user_dao.get_by_username(username='user1')
        print('\n', user)

    def test_update(self):
        user = self.user_dao.get(70)
        user.email = 'new@email.com'

        self.user_dao.update(user)

    def test_update_by_dict(self):
        user = {'id': 71, 'email': 'user31@gmail.com'}

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

    def test_delete_all(self):
        self.user_dao.delete_all()

    def test_merge(self):
        user = {'id': 51, 'username': 'user2', 'email': 'user2@gmail.com'}

        user = self.user_dao.merge(user)

        print(user)
