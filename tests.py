import unittest

from flask import abort, url_for
from flask_testing import TestCase

from app import create_app, db
from app.models import User, Role


class TestBase(TestCase):

    def create_app(self):
        # pass test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///C:\\Users\\Behruz D\\Documents\\stix-ui\\test_test.db'
        )

        return app

    def setUp(self):
        # will run before every test
        db.create_all()
        # create test admin user
        admin = User(username="admin", password="admin", is_admin=True)
        # create test user
        user = User(username="test", password="test")

        # save users to database
        db.session.add(admin)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        # will run after every test
        db.session.remove()
        db.drop_all()


class TestModels(TestBase):

    def test_user_model(self):
        # Test number of users in User table
        self.assertEqual(User.query.count(), 2)

    def test_role_model(self):
        # Test number of roles in Role table

        # create test role
        role = Role(name="analyst", description="analyze data")

        # save the role to database
        db.session.add(role)
        db.session.commit()

        self.assertEqual(Role.query.count(), 1)


class TestViews(TestBase):

    def test_homepage_view(self):
        # Test if homepage accessible without logging in
        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        # Test if login page is accessible without logging in
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        # Test if logout view is inaccessible without login, and redirects to login
        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_dashboard_view(self):
        # Test if dashboard view is inaccessible without login, and redirects to login
        target_url = url_for('home.dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_admin_dashboard_view(self):
        # Test if admin dashboard view is inaccessible without login, and redirects to login
        target_url = url_for('home.admin_dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_roles_view(self):
        # Test if roles view is inaccessible without login, and redirects to login
        target_url = url_for('admin.list_roles')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_users_view(self):
        # Test if users view is inaccessible without login, and redirects to login
        target_url = url_for('admin.list_users')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


class TestErrorPages(TestBase):

    def test_403_forbidden(self):
        # create route to abort the request with 403 error
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue(bytes("403 Error", encoding='utf-8') in response.data)

    def test_404_not_found(self):
        response = self.client.get('/nonexistingpage')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(bytes("404 Error", encoding='utf-8') in response.data)

    def test_500_internal_server_error(self):
        # create route to abort the request with 500 error
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue(bytes("500 Error", encoding='utf-8') in response.data)


if __name__ == '__main__':
    unittest.main()
