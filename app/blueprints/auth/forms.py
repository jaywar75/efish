# app/blueprints/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    SubmitField,
    BooleanField
)
# from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    """
    A registration form with optional 'existing_acct_id' dropdown
    that can be set to "NEW" or a valid account’s _id (as a string).
    """
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    email = StringField("Email")
    password = PasswordField("Password")
    confirm_password = PasswordField("Confirm Password")

    existing_acct_id = SelectField("Existing Account", choices=[], coerce=str)

    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email")
    password = PasswordField("Password")
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RequestResetForm(FlaskForm):
    email = StringField("Email")
    submit = SubmitField("Request Password Reset")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password")
    confirm_password = PasswordField("Confirm Password")
    submit = SubmitField("Reset Password")