from main.web.form.upload import UploadForm
from xflask.web import route
from xflask.web.controller import Controller
from xflask.web.response import Response


class FileController(Controller):

    @route('/api/upload', methods=['POST'])
    def upload(self, upload_form: UploadForm):
        print(upload_form)

        return Response.success()
