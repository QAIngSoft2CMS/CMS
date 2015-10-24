#!flask/bin/python
import os
import unittest
import time
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

class signuptestcase(unittest.TestCase):
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


class signintestcase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
        app.config['WTF_CSRF_ENABLED'] = False  
        app.config['SQLALCHEMY_RECORD_QUERIES'] = True
        self.client = app.test_client()
        ctx = app.app_context()
        ctx.push()
        db.create_all()
        return app


    def tearDown(self):        
        db.session.remove()
        db.drop_all()


    def test_signin_get(self):
        tester = app.test_client(self)
        response = tester.get('/auth/signin/', content_type='html/text')
        self.assertEqual(response.status_code, 200)


    def test_signin_post(self):

        user = User(username='testuser',
            email='test@example.com',
            password='test',
            role=1,
            status=1
            )
        db.session.add(user)
        db.session.commit()
        data = {'email': 'test@example.com',
                'password': 'test'
                }
        tester = app.test_client(self)
        response = tester.post(
            '/auth/signin/',
            data=data
        )
        self.assertTrue(response.status_code == 302)
        usertest = User.query.filter(User.username == 'Testuser').first()
        self.assertTrue(usertest.username == u'Testuser')


class tokentestcase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
        app.config['WTF_CSRF_ENABLED'] = False  
        app.config['SQLALCHEMY_RECORD_QUERIES'] = True
        self.client = app.test_client()
        ctx = app.app_context()
        ctx.push()
        db.create_all()
        return app

    def tearDown(self):        
        db.session.remove()
        db.drop_all()

    def test_generate_token(self):
        user = User(username='testuser',
            email='test@example.com',
            password='test',
            role=1,
            status=1
            )
        db.session.add(user)
        db.session.commit()
        with app.test_request_context():
            token = user.generate_token()
            self.assertTrue(user.verify_token(token) == user)
            #print "Token data is OK"


    def test_verify_token(self):
        user = User(username='testuser',
            email='test@example.com',
            password='test',
            role=1,
            status=1
            )
        db.session.add(user)
        db.session.commit()
        usertest = User.query.filter(User.username == 'Testuser').first()
        with app.test_request_context():
            token = user.generate_token(expiration=10)
            self.assertIs(user.verify_token(token),user)
            #print "We wait until the token expires"
            time.sleep(11)
            self.assertIsNot(user,usertest.verify_token(token))
            #print "Token expired after expected time"


class RecoverAccountTestCase(unittest.TestCase):
   
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
        app.config['WTF_CSRF_ENABLED'] = False  
        app.config['SQLALCHEMY_RECORD_QUERIES'] = True
        self.client = app.test_client()
        ctx = app.app_context()
        ctx.push()
        db.create_all()
        return app
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    #if you need a test_user use this in your function
    def initialize_test_user(self):
        usertest = User.query.filter(User.username == 'Testuser').first()
        if usertest==None:
            user = User(username='testuser',
                   email='is2testcms@gmail.com',
                   password='test',
                   role=1,
                   status=1
            )   
            db.session.add(user)
            db.session.commit()
    
            
    #in this pull request this team haven't a index page       
    def test_index(self):
        #self.initialize_test_user()
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 404)
    
    
    #Testing initialization of form recover password
    def test_init_recover_pass(self):
        tester = app.test_client(self)
        response = tester.get('/auth/recover_pass', content_type='html/text,',follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recuperar Cuenta', response.data)
    
        
    #Testing the correct function of recover password
    def test_recover_pass(self):
        self.initialize_test_user()
        tester = app.test_client(self)
        data = {'email': 'is2testcms@gmail.com'}
        response = tester.post(
            '/auth/recover_pass/',
            data= data,
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Se ha enviado un correo a la direccion',response.data)
    
    
    def test_change_password_recover(self):
        self.initialize_test_user()
        tester = app.test_client(self)
        usertest = User.query.filter(User.username == 'Testuser').first()
        token = usertest.get_token()
        old_password = usertest.password
        
        #test initialization of form Change Password
        url = '/auth/change_pass/?token='+str(token)
        response = tester.get(
            url,
            content_type='html/text,',follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Change Password', response.data)
        
        #Test functionality of Change Password
        data = {'password': 'new_test','confirm': 'new_test'}
        response_post = tester.post(
             url,
             data=data
        )
        self.assertIn(b'password updated successfully', response_post.data)
        self.assertIsNot(usertest.password, old_password)


class LogoutTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_RECORD_QUERIES'] = True
        self.client = app.test_client()
        ctx = app.app_context()
        ctx.push()
        db.create_all()
        return app


    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def initialize_test_user(self):
        usertest = User.query.filter(User.username == 'Testuser').first()
        if usertest==None:
            user = User(username='testuser',
                   email='test@example.com',
                   password='test',
                   role=1,
                   status=1
            )
            db.session.add(user)
            db.session.commit()
    
    
    def test_logout_remove_info(self):
        tester = app.test_client(self)
        response  = tester.get('/auth/logout', content_type='html/text')
        self.assertEqual(response.status_code, 301)


    def test_logout_redirect(self):
        self.initialize_test_user()
        tester = app.test_client(self)
        response = tester.post('/auth/logout/', content_type='html/text,', follow_redirects=True)

if __name__ == '__main__':
    unittest.main()
