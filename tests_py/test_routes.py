import unittest
from flask import Flask, url_for
from flask_testing import TestCase
from app import app, db, User

class FlaskTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_list_of_users_route(self):
        response = self.client.get(url_for('list_of_users'))
        self.assertEqual(response.status_code, 200)

    def test_new_user_form_route(self):
        response = self.client.get(url_for('new_user_form'))
        self.assertEqual(response.status_code, 200)

    def test_user_details_route(self):
        # Create a test user
        test_user = User(first_name='Test', last_name='User', image_url='test_image.jpg')
        db.session.add(test_user)
        db.session.commit()

        response = self.client.get(url_for('user_details', user_id=test_user.id))
        self.assertEqual(response.status_code, 200)

    def test_edit_user_route(self):
        # Create a test user
        test_user = User(first_name='Test', last_name='User', image_url='test_image.jpg')
        db.session.add(test_user)
        db.session.commit()

        response = self.client.get(url_for('edit_user', user_id=test_user.id))
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
