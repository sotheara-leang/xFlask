from test.test_case import *

from xflask.common import to_dict
from main.controller.vo.auth import LoginVo


class TestAuth(TestCase):

    def test_auth(self):
        login_vo = LoginVo('user1', '123')

        response = self.client.post('/api/login', json=to_dict(login_vo))

        json = response.json

        data = {'username': 'user2', 'password': '123', 'email': 'user2@example.com'}

        response = self.client.post('/api/user', json=to_dict(data),
                                   headers={'Authorization': 'Bearer ' + json.get('data').get('token')})

        print(response.json)






