from flask.ext.wtf import Form # , RecaptchaField
from wtforms import TextField, SubmitField  # BooleanField
from wtforms import TextAreaField, HiddenField, FileField,RadioField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import EqualTo, Length, Required
from models import db, Theme

strip_filter = lambda x: x.strip() if x else None

class ConfigurationThemeForm(Form):
    name           = HiddenField()
    default_use    = RadioField('Default?',
                               [Required()],
                                choices=[('yes', 'Default'), ('no', 'Not default')], default='yes'
                                )
    title          = TextField('Title',[Required("Please enter a title")],filters=[strip_filter])
    resources      = HiddenField()
    logo           = FileField('Plese entrer your image.png')
    description    = TextAreaField('description',[Required("Please enter a description")],
                        filters=[strip_filter])
    user_name      = HiddenField()
    

class UpdateTheme(Form):
	fileMarkdown = FileField('Plese entrer you Theme.md')

class SearchThemeForm(Form):
    name = TextField('Name Theme')
    id = TextField('Id Theme')
