# app/blueprints/user/forms.py

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    SelectField
)
from wtforms.validators import DataRequired, Email, Optional


class ViewProfileForm(FlaskForm):
    """
    A minimal form for showing all profile fields in read-only mode.
    Typically, you might not need a form at all if you’re only displaying data.
    However, if you want consistent structure (e.g., same fields as edit form),
    you can keep this form to show them.

    By default, we won't add validators that enforce requirements for display.
    """
    username = StringField("Username")
    email = StringField("Email")
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    phone = StringField("Phone")
    time_zone = StringField("Time Zone")
    about_me = TextAreaField("About Me")
    # Typically, no submit button is necessary on a "view-only" form,
    # unless you plan to have minimal interactive elements.
    # e.g., submit = SubmitField("Some Action")


class EditProfileForm(FlaskForm):
    """
    Form for editing the user’s profile details.
    Fields here mirror the data you want users to be able to update.
    """
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    first_name = StringField("First Name", validators=[Optional()])
    last_name = StringField("Last Name", validators=[Optional()])
    phone = StringField("Phone", validators=[Optional()])

    # If you want a predefined set of time zones, you could do:
    # time_zone = SelectField("Time Zone", choices=[
    #     ('UTC','UTC'),
    #     ('America/New_York','America/New_York'),
    #     ('Europe/London','Europe/London'),
    #     ...
    # ], validators=[Optional()])
    # Otherwise a free-text field:
    time_zone = StringField("Time Zone", validators=[Optional()])

    about_me = TextAreaField("About Me", validators=[Optional()])

    submit = SubmitField("Update Profile")