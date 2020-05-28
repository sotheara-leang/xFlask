from main.type.edu_level import EducationLevel

from xflask.wtforms import Form, PageForm
from xflask.wtforms import StringField, IntegerField, EnumField
from xflask.wtforms.validator import DataRequired, Length, Email, Optional


class UserForm(Form):
    id          = IntegerField(validators=[DataRequired()])
    username    = StringField(validators=[DataRequired(), Length(min=3, max=50)])
    password    = StringField(validators=[DataRequired(), Length(min=3, max=50)])
    email       = StringField(validators=[DataRequired(), Email()])
    edu_level   = EnumField(EducationLevel, validators=[DataRequired()])
    role_id     = IntegerField(validators=[DataRequired()])


class UserPageForm(PageForm):
    username    = StringField(default='', validators=[Optional()])
    edu_level   = EnumField(EducationLevel, default=None, validators=[Optional()])
    role_id     = IntegerField(default=None, validators=[Optional()])
