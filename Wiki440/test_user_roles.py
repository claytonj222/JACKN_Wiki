import os
import unittest
from wiki.web import create_app, current_wiki, current_users


class TestUserRoles(unittest.TestCase):
    """
    This class holds the unit tests for the user roles aspect of our Wiki system.
    It contains functions to test the user roles forms as well as the
    add_role function of the User class which is in the Wiki system.
    """
    def setUp(self):
        """
        This function just sets up some global things about the wiki like
        users and pages.
        """
        app = create_app(os.getcwd())

        app.config['TESTING'] = True
        with app.test_request_context():
            self.pages = current_wiki.index()
            self.users = current_users
            self.users.add_user('test', '1234')

    def test_add_role(self):
        """
        This test will check to make sure our test user has no roles
        assigned when he first gets created, and then will test that
        the add_role method is successfully adding a role to the user
        """
        self.assertEqual(self.users.get_user('test').get('roles'), [])
        self.users.get_user('test').add_role('admin')
        self.assertEqual(self.users.get_user('test').get('roles'), ['admin'])

    def test_is_admin_true(self):
        """
        This will add the admin role to our test user and then call
        the is_admin method to make sure that it is returning true
        """
        self.users.get_user('test').add_role('admin')
        self.assertTrue(self.users.get_user('test').is_admin())

    def test_is_admin_false(self):
        """
        This will make sure our test user has no roles and then call
        the is_admin method to make sure that it is returning false
        """
        self.users.get_user('test').set('roles', [])
        self.assertFalse(self.users.get_user('test').is_admin())

    def test_is_moderator_true(self):
        """
        This will add the moderator role to our test user and then call
        the is_moderator method to make sure that it is returning true
        """
        self.users.get_user('test').add_role('moderator')
        self.assertTrue(self.users.get_user('test').is_moderator())

    def test_is_moderator_false(self):
        """
        This will make sure our test user has no roles and then call
        the is_moderator method to make sure that it is returning false
        """
        self.users.get_user('test').set('roles', [])
        self.assertFalse(self.users.get_user('test').is_moderator())


if __name__ == '__main__':
    unittest.main()
