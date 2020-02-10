from test.test_case import *


class TestApiUser(TestCase):

    def test_getusers(self):
        response = self.client.get('/api/user')

        print('\n', response.json)

        self.assertIsNotNone(response.json)




