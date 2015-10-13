#!flask/bin/python
import os
import unittest
from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    g,
    session,
    redirect,
    url_for
)
from werkzeug import check_password_hash, generate_password_hash
from app import app, db
from app.authentication.models import User

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
        self.app = app.test_client()
        db.create_all()
        ctx = app.app_context()
        ctx.push()
        return app


    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def testsignupget(self):
        test = app.test_client(self)
        response = test.get('/auth/signup/', content_type='html/text')
        self.assertEqual(response.status_code, 200)


    def testsignuppost(self):
        new_user = User(username='testuser',
            email='test@example.com',
            password='test',
            role=1,
            status=1
            )
        db.session.add(new_user)
        db.session.commit()
        test = app.test_client(self)
        data={'username':'testuser','email':'test@example.com','password':'test'}
        response = test.post(
            '/auth/signup/',
            data=data
            )
        self.assertTrue(response.status_code == 200)
        usertest = User.query.filter(User.email == 'test@example.com').first()
        self.assertTrue(usertest.username == u'Testuser')


    def testfunctionhashpassword(self):
        new_user = User(username='testuser',
            email='test@example.com',
            password='test',
            role=1,
            status=1
            )
        db.session.add(new_user)
        db.session.commit()
        self.assertTrue(new_user.check_password('test'))


if __name__ == '__main__':
    unittest.main()
