from test.test_case import *

from main.controller.vo.user import UserVo
from main.type.edu_level import EducationLevel


class TestApiUser(TestCase):

    def test_get(self):
        response = self.client.get('/api/user/68')

        print('\n', response.json)

    def test_get_all(self):
        response = self.client.get('/api/user/')

        print('\n', response.json)

    def test_create(self):
        user = UserVo(username='user1', password='123',
                      role_id=1, email='user1@example.com', edu_level=EducationLevel.MASTER)

        response = self.client.post('/api/user/', json=user.serialize_())

        print('\n', response.json)

    def test_update(self):
        user = UserVo(id=60, username='user1', password='12345',
                      role_id=1, email='new@example.com', edu_level=EducationLevel.BACHELOR)

        response = self.client.put('/api/user', json=user.serialize_())

        print('\n', response.json)

    def test_delete(self):
        response = self.client.delete('/api/user/60')

        print('\n', response.json)
