from flask import request
from app import db
from app.authentication.models import User

class Theme(db.Model):
    __tablename__ = 'theme'
    id            = db.Column('id', db.Integer, primary_key=True, autoincrement='ignore_fk')
    name          = db.Column(db.String(100))
    default_use   = db.Column(db.Boolean)
    title         = db.Column(db.String(100))
    logo          = db.Column(db.String(100))
    resources     = db.Column(db.String(100))
    description   = db.Column(db.Text)
    user_name     = db.Column(db.String(10), db.ForeignKey(User.username))


    def __init__(self, name, default_use, title,logo,resources,description,user_name):
        self.name           = name
        self.deafult_use    = default_use
        self.title          = title
        self.logo           = logo
        self.resources      = resources
        self.description    = description
        self.user_name      = user_name
