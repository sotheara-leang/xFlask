from xflask.wtforms import FileField, FileRequired, EnumField, StringField
from xflask.wtforms import Form

from main.type.file import FileType


class UploadForm(Form):
    file        = FileField(validators=[FileRequired()])
    file_name   = StringField()
    type        = EnumField(FileType)
