# app/blueprints/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# from wtforms.validators import (
#     DataRequired,
#     Length,
#     Email,
#     EqualTo,
#     ValidationError
# )
# from app.models.user import User

class RegistrationForm(FlaskForm):
    """
    We have removed all validations and custom validation methods.
    In a future release, you can re-introduce validators as needed.
    """
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    email = StringField("Email")
    password = PasswordField("Password")
    confirm_password = PasswordField("Confirm Password")
    submit = SubmitField("Sign Up")

    # def validate_username(self, username):
    #     user = User.get_by_username(username.data)
    #     if user:
    #         raise ValidationError("That username is taken.")

    # def validate_email(self, email):
    #     user = User.get_by_email(email.data)
    #     if user:
    #         raise ValidationError("That email is already registered.")


class LoginForm(FlaskForm):
    """
    A stripped-down login form without any field-level validators.
    """
    email = StringField("Email")
    password = PasswordField("Password")
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RequestResetForm(FlaskForm):
    """
    Password-reset request form with no validations.
    """
    email = StringField("Email")
    submit = SubmitField("Request Password Reset")

    # def validate_email(self, email):
    #     user = User.get_by_email(email.data)
    #     if user is None:
    #         raise ValidationError("There is no account with that email. Please register first.")


class ResetPasswordForm(FlaskForm):
    """
    A form for setting a new password, with all validations removed.
    """
    password = PasswordField("Password")
    confirm_password = PasswordField("Confirm Password")
    submit = SubmitField("Reset Password")