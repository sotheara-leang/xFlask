from xflask.wtforms import Form
from xflask.wtforms import StringField
from xflask.wtforms.validator import InputRequired, Length


class LoginForm(Form):
    username = StringField(validators=[InputRequired(), Length(min=3, max=50)])
    password = StringField(validators=[InputRequired(), Length(min=3, max=50)])
