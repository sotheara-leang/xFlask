from xflask.wtforms import FileField, FileRequired
from xflask.wtforms import Form


class UploadForm(Form):
    file = FileField(validators=[FileRequired()])
