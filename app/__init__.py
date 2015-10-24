# Import flask and template operators
from flask import Flask, render_template
from flask_mail import Mail
# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Import Bower
from flask.ext.bower import Bower

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

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

# Register blueprint(s)
app.register_blueprint(auth_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
