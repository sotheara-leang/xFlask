from test.test_case import *


class TestAuth(TestCase):

    def test_auth(self):
        request = {'username': 'user1', 'password': ''}

        response = self.client.post('/api/login', json=request)

        print('\n', response.json)







