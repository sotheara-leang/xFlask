from test.test_case import *


class TestAuth(TestCase):

    def test_auth(self):
        request = {'username': 'user3', 'password': '123'}

        response = self.client.post('/api/login', json=request)

        token = response.json['data']['token']

        print('\n', token)

        response = self.client.get('/api/user/', headers={"Authorization": "Bearer {}".format(token)})

        print('\n', response.json)


    def test_logout(self):
        request = {'username': 'user3', 'password': '123'}

        response = self.client.post('/api/login', json=request)

        token = response.json['data']['token']

        print('\n', token)

        response = self.client.post('/api/logout', headers={"Authorization": "Bearer {}".format(token)})

        print('\n', response.json)






