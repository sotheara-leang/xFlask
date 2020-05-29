from xflask.wtforms import Form
from xflask.wtforms import StringField
from xflask.wtforms.validator import DataRequired, Length


class LoginForm(Form):
    username = StringField(validators=[DataRequired(), Length(min=3, max=50)])
    password = StringField(validators=[DataRequired(), Length(min=3, max=50)])
