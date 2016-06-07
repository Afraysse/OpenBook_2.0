import unittest
from unittest import TestCase
from model import connect_to_db, db, User, Draft, Published
from server import app
import server
from mock import MagicMock 


class FlaskTestsLoggedIn(TestCase):
    """Flask tests when user is logged into session"""

    def setUp(self):
        """Prior to running test"""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'

        self.client = app.test_client()
        connect_to_db(app, "postgresql:///openbook")

        #Creates tables and adds in sample data

        db.drop_all()
        db.create_all()
        example_data()
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def test_login(self):
        """Test login page"""

        result = self.client.get('/profile/1')
        self.assertIn("Age", result.data)

    def test_home(self):
        """Test login."""

        result = self.client.get("/")
        self.assertIn("Dashboard", result.data)
        self.assertNotIn("Log In", result.data)



class MyAppIntegrationTestCase(TestCase):

    def test_homepage(self):
        test_client = server.app.test_client()
        result = test_client.get('/')
        self.assertIn('<h5>Login</h5>', result.data)

