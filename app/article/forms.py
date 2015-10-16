from flask.ext.wtf import Form # , RecaptchaField
from wtforms import TextField, PasswordField, SubmitField  # BooleanField
from wtforms import TextAreaField, HiddenField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Email, EqualTo, Length, Regexp
from app.sections.models import Sections

strip_filter = lambda x: x.strip() if x else None

def section_choice():
    return Sections.query.all()

class ArticleCreateForm(Form):
    title     = TextField('Title', [Required("Please enter a title")],
                        filters=[strip_filter])
    body      = TextAreaField('Body',[Required("Please enter a body")],
                        filters=[strip_filter])
    section   = QuerySelectField('Section', query_factory=section_choice )
    user_name = HiddenField()

class ArticleUpdateForm(Form):
    id = HiddenField()

class SectionCreateForm(Form):
    name = TextField('Name', [validators.Length(min=1,max=240)])
    description = TextAreaField('Description')
