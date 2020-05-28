from test.test_case import *


class TestAuth(TestCase):

    def test_auth(self):
        request = {'username': 'user1', 'password': '123'}

        response = self.client.post('/api/login', json=request)

        print('\n', response.json)







