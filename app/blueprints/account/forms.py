# app/blueprints/account/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class EditAccountForm(FlaskForm):
    account_name = StringField("Account Name")
    plan_type = StringField("Plan Type")
    submit = SubmitField("Update")