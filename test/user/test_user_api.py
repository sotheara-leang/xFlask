from test.test_case import *

from main.type.edu_level import EducationLevel


class TestApiUser(TestCase):

    def test_get(self):
        response = self.client.get('/api/user/6')

        print('\n', response.json)

    def test_get_all(self):
        response = self.client.get('/api/user/')

        print('\n', response.json)

    def test_get_page(self):
        data = dict(
            page=1,
            per_page=20,
            username='',
            edu_level='',
            role_id='',
            sort=[dict(
                field='username',
                order='asc'
            )]
        )

        response = self.client.post('/api/user/page', json=data)

        print('\n', response.json)

    def test_create(self):
        user = dict(username='user1', password='123', role_id=1,
                    email='user1@example.com', edu_level=EducationLevel.MASTER.code())

        response = self.client.post('/api/user/', json=user)

        print('\n', response.json)

    def test_update(self):
        user = dict(id=1, username='user2', password='ggggg', role_id=1,
                    email='new@example1.com', edu_level=EducationLevel.BACHELOR.code())

        response = self.client.put('/api/user/', json=user)

        print('\n', response.json)

    def test_delete(self):
        response = self.client.delete('/api/user/60')

        print('\n', response.json)
