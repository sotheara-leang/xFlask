from main.type.edu_level import EducationLevel

from xflask.wtforms import Form, PageForm
from xflask.wtforms import StringField, IntegerField, EnumField
from xflask.wtforms.validator import Length, Email, InputRequired


class UserForm(Form):
    id          = IntegerField(validators=[InputRequired()])
    username    = StringField(validators=[InputRequired(), Length(min=3, max=50)])
    password    = StringField(validators=[InputRequired(), Length(min=3, max=50)])
    email       = StringField(validators=[InputRequired(), Email()])
    edu_level   = EnumField(EducationLevel, validators=[InputRequired()])
    role_id     = IntegerField(validators=[InputRequired()])


class UserPageForm(PageForm):
    username    = StringField(default=None)
    edu_level   = EnumField(EducationLevel, default=None)
    role_id     = IntegerField(default=None)
