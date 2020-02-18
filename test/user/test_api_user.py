from test.test_case import *
from xflask.common.json_util import to_dict

from main.controller.vo.user import *


class TestApiUser(TestCase):

    def test_get(self):
        response = self.client.get('/api/user/49')

        print('\n', response.json)

    def test_get_all(self):
        response = self.client.get('/api/user')

        print('\n', response.json)

    def test_create(self):
        user = CreateUserVo(username='user1', password='123', role_id=1,
                    email='user1@example.com')

        response = self.client.post('/api/user', json=to_dict(user, True))

        print('\n', response.json)

    def test_delete(self):
        response = self.client.delete('/api/user/49')

        print('\n', response.json)
