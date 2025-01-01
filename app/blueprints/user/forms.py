# app/blueprints/user/forms.py

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    SubmitField,
    SelectField
    # If you decide to reintroduce time-zone choices in the future,
    # you can re-add other validators or fields
)

# ------------------------------------------------------------
# Registration Form
# ------------------------------------------------------------
class RegistrationForm(FlaskForm):
    """
    For creating a new user account (with minimal fields).
    Validators are commented out for now,
    so no required or email checks are enforced.
    """
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    email = StringField("Email")
    password = PasswordField("Password")
    # confirm_password = PasswordField("Confirm Password")

    # New dropdown for selecting an existing account (or "NEW"), populated in the route
    existing_acct_id = SelectField("Existing Account", choices=[], coerce=str)

    submit = SubmitField("Register")


# ------------------------------------------------------------
# View Profile Form
# ------------------------------------------------------------
class ViewProfileForm(FlaskForm):
    """
    A minimal form for displaying user profile fields in read-only mode.
    Currently no validators are used for display purposes.
    """
    email = StringField("Email")
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    phone = StringField("Phone")
    time_zone = StringField("Time Zone")
    about_me = TextAreaField("About Me")
    # Typically, a view-only form doesn't need a submit button,
    # unless you plan to include interactive elements.


# ------------------------------------------------------------
# Edit Profile Form
# ------------------------------------------------------------
class EditProfileForm(FlaskForm):
    """
    A form for editing the user’s profile details.
    """
    email = StringField("Email")
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    phone = StringField("Phone")

    # If you plan to offer a dropdown for time zones in the future,
    # you can uncomment and use a SelectField, etc.
    time_zone = StringField("Time Zone")

    about_me = TextAreaField("About Me")

    submit = SubmitField("Update Profile")