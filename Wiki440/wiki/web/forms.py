"""
    Forms
    ~~~~~
"""
from flask_wtf import Form
from wtforms import BooleanField
from wtforms import TextField
from wtforms import TextAreaField
from wtforms import PasswordField
from wtforms.validators import InputRequired
from wtforms.validators import ValidationError

from wiki.core import clean_url
from wiki.web import current_wiki
from wiki.web import current_users


class URLForm(Form):
    url = TextField('', [InputRequired()])

    def validate_url(form, field):
        if current_wiki.exists(field.data):
            raise ValidationError('The URL "%s" exists already.' % field.data)

    def clean_url(self, url):
        return clean_url(url)


class SearchForm(Form):
    term = TextField('', [InputRequired()])
    ignore_case = BooleanField(
        description='Ignore Case',
        # FIXME: default is not correctly populated
        default=True)


class EditorForm(Form):
    title = TextField('', [InputRequired()])
    body = TextAreaField('', [InputRequired()])
    tags = TextField('')


class LoginForm(Form):
    name = TextField('', [InputRequired()])
    password = PasswordField('', [InputRequired()])

    def validate_name(form, field):
        user = current_users.get_user(field.data)
        if not user:
            raise ValidationError('This username does not exist.')

    def validate_password(form, field):
        user = current_users.get_user(form.name.data)
        if not user:
            return
        if not user.check_password(field.data):
            raise ValidationError('Username and password do not match.')


class AddRoleForm(Form):
    name = TextField('', [InputRequired()])
    role = TextField('', [InputRequired()])


def user_already_exists(name, user_manager):
    """
    Helper function to test if user already exists in user_manager
    """
    return user_manager.get_user(name) is not None


def passwords_match(password, confirmation):
    """
    Helper function to test if password strings match
    """
    return password == confirmation


class CreateUserForm(Form):
    """
    This class represents the form which is used to create a new user.
    It consists of three fields:

    name - A TextField which is the users name
    password - A PasswordField which is the users password
    confirm_password - A PasswordField which makes the user double check their typed password

    All three fields are required on the form
    """
    name = TextField('', [InputRequired()])
    password = PasswordField('', [InputRequired()])
    confirm_password = PasswordField('', [InputRequired()])

    def validate_name(form, field):
        """
        This function exists to validate the name entered by the user. Since
        a name is unique, we must make sure the user does not already exist by the same name.
        """
        if user_already_exists(field.data, current_users):
            raise ValidationError('User already exists, please try a different name.')

    def validate_password(form, field):
        """
        This function exists to do two types of validation:
        - First it checks if the password the user entered is empty and will fail if that is true.
        - If the password is not empty, this function checks to make sure that it matches the confirm password field
        """
        if field.data == '':
            raise ValidationError('Password cannot be empty!')
        if not passwords_match(field.data, form.confirm_password.data):
            raise ValidationError('Passwords do not match!')
