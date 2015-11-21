# Import flask and template operators
from flask import Flask, render_template
from flask_mail import Mail
# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy
import os

# Import Bower
from flask.ext.bower import Bower

# Define the WSGI application object
app = Flask(__name__,template_folder='templates')


# Configurations
app.config.from_object('config')

APP_ROOT = os.path.dirname(os.path.abspath(__name__))
APP_STATIC = os.path.join(APP_ROOT, 'themes/static')
app.config['UPLOAD_FOLDER'] = APP_STATIC

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Initiate Bower
Bower(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

db.create_all()

app.config['MAIL_SERVER'] = 'evop5.areserver.net'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'pruebas.cms@asacoop.com'
app.config['MAIL_PASSWORD'] = 'admin1234'
mail=Mail(app)

# Import a module / component using its blueprint handler variable (mod_auth)
from app.authentication.controllers import mod_auth as auth_module
from app.themes.controllers import mod_theme as theme_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(theme_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
