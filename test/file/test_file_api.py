from test.test_case import *

from werkzeug.datastructures import FileStorage
from main.type.file import FileType


class TestApiFile(TestCase):

    def test_upload(self):
        file = FileStorage(
            stream=open('sample.txt', "rb")
        )
        data = dict(
            file=file,
            type=FileType.PDF.code(),
            file_name='222'
        )
        response = self.client.post('/api/upload', data=data, content_type='multipart/form-data')

        print('\n', response.data)
