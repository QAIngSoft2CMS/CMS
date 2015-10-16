import datetime
from flask import request
from app import db
from app.sections.models import Sections
from app.authentication.models import User



class Article(db.Model):
    __tablename__ = 'article'
    id              = db.Column('id', db.Integer, primary_key=True, autoincrement='ignore_fk')
    title           = db.Column(db.String(100))
    body            = db.Column(db.Text)
    created         = db.Column(db.DateTime, default=datetime.datetime.now)
    section_name    = db.Column(db.String(10), db.ForeignKey(Sections.section_name))
    section         = db.relationship(Sections)
    user_name       = db.Column(db.String(100), db.ForeignKey(User.username, onupdate="CASCADE",
                        ondelete="CASCADE"))
    user            = db.relationship(User)

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
