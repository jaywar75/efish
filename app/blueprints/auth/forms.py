# app/blueprints/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError
)
from app.models.user import User

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=2, max=20)
    ])
    email = StringField("Email", validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(),
        EqualTo("password")
    ])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        # Previously, this called `User.get_by_email(username.data)`.
        # Now we correctly query by username:
        user = User.get_by_username(username.data)
        if user:
            raise ValidationError("That username is taken. Please choose a different one.")

    def validate_email(self, email):
        user = User.get_by_email(email.data)
        if user:
            raise ValidationError("That email is already registered.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField("Password", validators=[
        DataRequired()
    ])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[
        DataRequired(),
        Email()
    ])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.get_by_email(email.data)
        if user is None:
            raise ValidationError("There is no account with that email. You must register first.")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(),
        EqualTo("password")
    ])
    submit = SubmitField("Reset Password")