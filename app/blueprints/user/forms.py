# app/blueprints/user/forms.py

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField
    # If you decide to reintroduce time-zone choices in the future,
    # you can re-add: SelectField
)


class ViewProfileForm(FlaskForm):
    """
    A minimal form for displaying user profile fields in read-only mode.
    By default, we won’t add validations for display purposes.
    """
    email = StringField("Email")
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    phone = StringField("Phone")
    time_zone = StringField("Time Zone")
    about_me = TextAreaField("About Me")
    # Typically, a view-only form doesn't need a submit button,
    # unless you plan to include interactive elements.


class EditProfileForm(FlaskForm):
    """
    A form for editing the user’s profile details.
    """
    email = StringField("Email")
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    phone = StringField("Phone")

    # If you plan to offer a dropdown for time zones in the future,
    # you can uncomment and use SelectField:
    # time_zone = SelectField(
    #     "Time Zone",
    #     choices=[
    #         ('UTC','UTC'),
    #         ('America/New_York','America/New_York'),
    #         ('Europe/London','Europe/London'),
    #         ...
    #     ]
    # )
    time_zone = StringField("Time Zone")

    about_me = TextAreaField("About Me")

    submit = SubmitField("Update Profile")