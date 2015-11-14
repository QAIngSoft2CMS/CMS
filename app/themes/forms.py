from flask.ext.wtf import Form # , RecaptchaField
from wtforms import TextField, SubmitField  # BooleanField
from wtforms import TextAreaField, HiddenField, FileField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import EqualTo, Length
from models import db, Theme


class ConfigurationTheme(Form):
	#name           = TextField('Theme', [Required("Please enter a theme")],
	#					filters=[strip_filter])
	#default_use    = RadioField('Default?',
	#		       			 [validators.Required()],
	#		        		 choices=[('yes', 'Default'), ('no', 'Not default')], default='yes'
	#		                )
    #title          = TextField('Title', [Required("Please enter a title")],
    #                    filters=[strip_filter])
    #resources      = HiddenField()
    #logo           = FileField()
    #description    = TextAreaField('description',[Required("Please enter a description")],
    #                    filters=[strip_filter])
    user_name      = HiddenField()

	#def __init__(self, *args, **kwargs):
	#    Form.__init__(self, *args, **kwargs)


class UpdateTheme(Form):
	fileMarkdown = FileField('Plese entrer you Theme.md')
