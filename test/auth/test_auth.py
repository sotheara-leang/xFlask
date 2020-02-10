from test.test_case import *

from xflask.common.util import to_dict
from main.controller.vo.auth import LoginVo


class TestAuth(TestCase):

    def test_auth(self):
        login_vo = LoginVo('user1', '123')

        response = self.client.post('/api/login', json=to_dict(login_vo))

        print('\n', response.json)

        self.assertIsNotNone(response.json)




