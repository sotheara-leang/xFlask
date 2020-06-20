from xflask.wtforms import FileField, FileRequired, EnumField
from xflask.wtforms import Form

from main.type.file import FileType


class UploadForm(Form):
    file = FileField(validators=[FileRequired()])
    type = EnumField(FileType)
