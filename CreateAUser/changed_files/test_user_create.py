import os
import unittest
from wiki.web import create_app, current_wiki, current_users
from wiki.web.forms import CreateUserForm, TextField, PasswordField
from wtforms.validators import ValidationError


class TestCreateUser(unittest.TestCase):

    def setUp(self):

        app = create_app(os.getcwd())

        app.config['TESTING'] = True
        with app.test_request_context():
            self.pages = current_wiki.index()
            self.users = current_users

    def test_user_create_form_name_validation(self):
        form = CreateUserForm()
        form.name = TextField('alex')
        self.assertRaises(ValidationError, form.validate_name(form.name))

    def test_user_create_form_password_validation(self):
        form = CreateUserForm()
        form.password = PasswordField('1234')
        form.confirm_password = PasswordField('12345')
        self.assertRaises(ValidationError, form.validate_password(form.password))

    def test_create_user(self):
        self.users.create_user('tester', 'testing123')
        self.assertIsNotNone(self.users.get_user('tester'))

if __name__ == '__main__':
    unittest.main()
