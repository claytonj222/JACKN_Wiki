import os
import unittest
from wiki.web import create_app, current_wiki, current_users
from wiki.web.forms import CreateUserForm, TextField, PasswordField
from wtforms.validators import ValidationError


class TestCreateUser(unittest.TestCase):
    """
    This class holds the unit tests for the user creation aspect of our Wiki system.
    It contains functions to test the user creation forms as well as the
    create_user function of the UserManager class which is in the Wiki system.
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

    def test_user_create_form_name_validation(self):
        """
        This test makes sure that the CreateUserForm validates the
        input name and make sure it doesn't already exist in the system.
        """
        form = CreateUserForm()
        form.name = TextField('alex')
        self.assertRaises(ValidationError, form.validate_name(form.name))

    def test_user_create_form_password_validation(self):
        """
        This test makes sure that the CreateUserForm validates that the password
        entered by the user does not differ from the confirm_password.
        """
        form = CreateUserForm()
        form.password = PasswordField('1234')
        form.confirm_password = PasswordField('12345')
        self.assertRaises(ValidationError, form.validate_password(form.password))

    def test_create_user(self):
        """
        This test makes sure the create user function works when being passed a user
        by the name of 'tester'
        """
        self.users.create_user('tester', 'testing123')
        self.assertIsNotNone(self.users.get_user('tester'))

if __name__ == '__main__':
    unittest.main()
