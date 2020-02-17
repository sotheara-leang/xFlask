from test.test_case import *

from main.model.user import User
from main.type.edu_level import EducationLevel


class TestApiUser(TestCase):

    def test_get(self):
        response = self.client.get('/api/user/49')

        print('\n', response.json)

    def test_get_all(self):
        response = self.client.get('/api/user')

        print('\n', response.json)

    def test_create(self):
        user = User(username='user1', password='123',
                    email='user1@example.com', edu_level=EducationLevel.BACHELOR)

        response = self.client.post('/api/user', json=user.to_dict())

        print('\n', response.json)

    def test_delete(self):
        response = self.client.delete('/api/user/49')

        print('\n', response.json)
