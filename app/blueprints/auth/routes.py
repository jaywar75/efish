# app/blueprints/auth/routes.py

import secrets
from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    current_app
)
from flask_login import (
    login_user,
    current_user,
    logout_user,
    login_required
)
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from werkzeug.security import generate_password_hash
from flask_mail import Message

# Existing blueprint import
from app.blueprints.auth import auth_bp

# Existing forms
from app.blueprints.auth.forms import (
    RegistrationForm,
    LoginForm,
    RequestResetForm,
    ResetPasswordForm
)

# Newly added: to integrate existing account or "NEW" logic
from app.blueprints.services.user_service import create_user_with_account_option

# Existing imports
from app.models.user import User
from app.extensions import mongo, mail


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    A registration route that:
      - Provides a dropdown for selecting an existing account or creating a new account.
      - Collects first_name, last_name, email, password.
      - Inserts a new user doc referencing the chosen or newly created account in MongoDB.
      - Redirects to the login page on success.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegistrationForm()

    # Query all existing accounts
    accounts = mongo.db.accounts.find({})
    # Build choices: the user can pick an existing account OR "NEW"
    acct_choices = [("NEW", "Generate New Account")]
    for acct in accounts:
        label = acct.get("account_name", str(acct["_id"]))
        acct_choices.append((str(acct["_id"]), label))

    # Assign these to the dropdown
    form.existing_acct_id.choices = acct_choices

    if form.validate_on_submit():
        new_user_id = create_user_with_account_option(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data,
            existing_acct_id=form.existing_acct_id.data  # "NEW" or a valid 24-hex ID
        )
        flash("User registered!", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    A minimal login route that:
      - Looks up the user by email.
      - Verifies the hashed password.
      - Redirects to a 'dashboard' or home page on success.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        # Find user by email
        user_doc = mongo.db.users.find_one({"email": form.email.data.lower()})
        if not user_doc:
            flash("Invalid email or password", "danger")
            return render_template("login.html", form=form)

        # Convert doc to User model
        user_obj = User(user_doc)

        # Check password
        if user_obj.verify_password(form.password.data):
            login_user(user_obj)
            flash("Login successful!", "success")
            return redirect(url_for("main.dashboard"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html", form=form)


@auth_bp.route("/logout")
def logout():
    """
    A basic logout route that logs the user out and redirects to the login.
    """
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/reset_request", methods=["GET", "POST"])
def reset_request():
    """
    Handles requesting a password reset via email.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RequestResetForm()
    if form.validate_on_submit():
        user_doc = mongo.db.users.find_one({"email": form.email.data.lower()})
        if user_doc:
            user_obj = User(user_doc)
            send_reset_email(user_obj)

        # For security, do not reveal if email doesn't exist
        flash("If the account exists, you will receive a password-reset email.", "info")
        return redirect(url_for("auth.login"))

    return render_template("reset_request.html", form=form)


@auth_bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """
    Handles the actual password-reset form (via token link).
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        # The token stores the user's email (or user ID).
        email = s.loads(token, max_age=1800)  # 30 min expiry
    except SignatureExpired:
        flash("Your reset link has expired. Please request a new one.", "warning")
        return redirect(url_for("auth.reset_request"))
    except BadSignature:
        flash("Invalid token. Please request a new reset link.", "danger")
        return redirect(url_for("auth.reset_request"))

    user_doc = mongo.db.users.find_one({"email": email})
    if not user_doc:
        flash("Could not find a matching user. Contact support.", "danger")
        return redirect(url_for("auth.reset_request"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        mongo.db.users.update_one(
            {"_id": user_doc["_id"]},
            {"$set": {"password_hash": hashed_pw}}
        )
        flash("Your password has been updated! You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("reset_password.html", form=form)


def send_reset_email(user_obj):
    """
    A helper function that:
      1. Generates a token for the user.
      2. Sends an email containing the reset link to that user.
    """
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    token = s.dumps(user_obj.email)  # embed the email in the token

    # Example: http://127.0.0.1:5000/auth/reset_password/<token>
    reset_url = url_for("auth.reset_password", token=token, _external=True)

    subject = "Password Reset Request"
    sender = current_app.config.get("MAIL_DEFAULT_SENDER", "no-reply@example.com")
    recipients = [user_obj.email]

    # If your user model has first_name:
    body = f"""\
Hello {user_obj.first_name},

You requested a password reset. Please visit the link below to set a new password:
{reset_url}

If you did not request this reset, simply ignore this email.

Thanks,
Your Support Team
"""

    msg = Message(subject=subject, sender=sender, recipients=recipients, body=body)
    mail.send(msg)