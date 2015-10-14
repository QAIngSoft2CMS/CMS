import datetime
from flask import request
from app import db
from werkzeug import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)




class User(db.Model):

    __tablename__ = 'auth_user'
    
    id       = db.Column('id', db.Integer, primary_key=True, \
                autoincrement='ignore_fk')
    username = db.Column(db.String(128),  nullable=False, unique=True)
    email    = db.Column(db.String(128),  nullable=False, unique=True)
    password = db.Column(db.String(128),  nullable=False)
    role     = db.Column(db.SmallInteger, nullable=False)
    status   = db.Column(db.SmallInteger, nullable=False)

    def __init__(self, username, email, password,role,status):

        self.username = username.title()
        self.email    = email.lower()
        self.password = generate_password_hash(password)
        self.role     = role
        self.status   = status

    def __repr__(self):
        return '<User %r>' % (self.username)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_token(self, expiration = 600):
        s = Serializer('key_word', expires_in = expiration)
        return s.dumps({'id': self.id, 'username':self.username, \
        'email':self.email,'ip_address': request.remote_addr})

    @staticmethod
    def verify_token(token):
        s = Serializer('key_word')
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

class Section(db.Model):
    __tablename__ = 'section'
    id            = db.Column('id', db.Integer, primary_key=True, autoincrement='ignore_fk')
    name          = db.Column(100.String(100), unique=True)
    description   = db.Column(db.Text)

    def __unicode__(self):
        return self.name

class Article(db.Model):
    __tablename__ = 'articles'
    id        = db.Column('id', db.Integer, primary_key=True, autoincrement='ignore_fk')
    title     = db.Column(db.String(100))
    body      = db.Column(db.Text)
    created   = db.Column(db.DateTime, default=datetime.datetime.now)
    section_name = db.Column(db.String(10), db.ForeignKey(Section.name))
    section   = db.relationship(Section)
    user_name = db.Column(db.String(100), db.ForeignKey(User.username, onupdate="CASCADE",
                        ondelete="CASCADE"))
    user      = db.relationship(User)

    @classmethod
    def all(cls):
        return Article.query_order_by(desc(Article.created)).all()

    @classmethod
    def find_by_id(cls, id):
        return Article.query.filter(Article.id == id).first()

    @classmethod
    def find_by_author(cls, name):
        return Article.query.filter(Article.user_name == name).all()

    @classmethod
    def find_by_section(cls, section):
        return Article.query.filter(Article.category_name == section).all()

    @property
    def slug(self):
        return urlify(self.title)

    @property
    def created_in_words(self):
        return time_ago_in_words(self.created)
