from wtforms import *
from wtforms.validators import *

from flask_wtf import FlaskForm
from flask_wtf.file import *

from .field import *


class Form(FlaskForm):

    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
