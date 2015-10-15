from flask.ext.wtf import Form # , RecaptchaField
from wtforms import TextField, PasswordField, SubmitField  # BooleanField
from wtforms import TextAreaField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Email, EqualTo, Length, Regexp
from models import db, User, Section

strip_filter = lambda x: x.strip() if x else None

def section_choice():
    return Section.query.all()

class ArticleCreateForm(Form):
    title     = TextField('Title', [Required("Please enter a title")],
                        filters=[strip_filter])
    body      = TextAreaField('Body',[Required("Please enter a body")],
                        filters=[strip_filter])
    section   = QuerySelectField('Section', query_factory=section_choice )
    user_name = HiddenField()

class ArticleUpdateForm(Form):
    id = HiddenField()


class SignupForm(Form):
    username = TextField('Username', [Length(min=6, max=25), Regexp(r'^[\w]+$'),
            Required(message='Please enter an username.')])
    email    = TextField('Email Address', [Email(),
                Required(message='Please enter your email address.')])
    password = PasswordField('Password', [Length(min=6, max=25),
                Required(message='Please enter a password.')])
    submit   = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken.")
        else:
            return True

class LoginForm(Form):
    email    = TextField('Email Address', [Email(),
                Required(message='Forgot your email address?')])
    password = PasswordField('Password', [
                Required(message='Must provide a password.')])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email = self.email.data).first()
        if(user is None):
            self.email.errors.append("That email is not registered.")
        elif (user.check_password(self.password.data)):
            return True
        else:
            self.password.errors.append("Incorrect Password")
        return False

class SectionCreateForm(Form):
    name = TextField('Name', Length(min=1,max=240))
    description = TextAreaField('Description')
