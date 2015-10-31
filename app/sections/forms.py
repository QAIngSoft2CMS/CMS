from flask.ext.wtf import Form # , RecaptchaField
from wtforms import StringField, BooleanField, PasswordField, TextField , TextAreaField # BooleanField
from wtforms.validators import Required, DataRequired, Email, EqualTo

class CreateSectionForm(Form):
	section = StringField('section', validators=[DataRequired()])
	description = TextAreaField('description')


class EditSectionForm(Form):
	section = StringField('section', validators=[DataRequired()])
	description = TextAreaField('description')