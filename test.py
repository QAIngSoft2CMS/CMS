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
from app import app, db
from app.article.models import Article
from app.authentication.models import User
from app.sections.models import Sections

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class createarticlecase(unittest.TestCase):
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


    def testarticlecreatepost(self):
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
            token = user.generate_token()
        new_article = Article(title='testtitle',
            body='testbody',
            user_name=usertest.username,
            user=usertest,
            )
        db.session.add(new_article)
        db.session.commit()
        test = app.test_client(self)
        self.assertTrue(new_article.find_by_id(new_article.id)!= None)
        self.assertTrue(new_article.find_by_author(new_article.user_name)!= None)


class articlemodelcase(unittest.TestCase):
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


    def testarticlecreatepost(self):
        user = User(username='testuser',
            email='test@example.com',
            password='test',
            role=1,
            status=1
            )
        db.session.add(user)
        db.session.commit()
        testsection = Sections(section_='sectionname',description_='section created to test an article') 
        db.session.add(testsection)
        db.session.commit()
        usertest = User.query.filter(User.username == 'Testuser').first()
        testarticle = Article(title='testtitle',
            body='testbody',
            section_name = testsection.section_name,
            section = testsection,
            user_name=usertest.username,
            user=usertest,
            )
        db.session.add(testarticle)
        db.session.commit()
        test = app.test_client(self)
        #self.assertTrue(testarticle.all()!= None)
        self.assertTrue(testarticle.find_by_id(testarticle.id)!= None)
        self.assertTrue(testarticle.find_by_author(testarticle.user_name)!= None)
        self.assertTrue(testarticle.find_by_section('testsection')!= None)

class CreateAndViewSectionsTestCase(unittest.TestCase):
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
    
    #testing view sections
    def test_view_sections(self):

        tester = app.test_client(self)
        response = tester.get('/sec/views_sections/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    
    #testing create sections
    def test_get_create_sections(self):

        tester = app.test_client(self)
        response = tester.get('/sec/create_sections/', content_type='html/text')
        self.assertIn(b'Digite el nombre de la nueva seccion',response.data)
        self.assertEqual(response.status_code, 200)
     
    # now testing the post method to create sections    
    def test_post_create_sections(self):
        tester = app.test_client(self)

        data = {'section': 'example of test section', 'description': 'example of description'}
        response = tester.post(
             '/sec/create_sections/',
             data= data,
             follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Example Of Test Section', response.data)
        self.assertIn(b'example of description', response.data)


if __name__ == '__main__':
    unittest.main()
