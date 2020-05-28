from flask_wtf import FlaskForm


class Form(FlaskForm):

    class Meta:
        csrf = False

    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)

        exclude = kwargs.get('exclude') or []
        self.exclude = exclude
