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
from app.blueprints.auth import auth_bp
from app.blueprints.auth.forms import (
    RegistrationForm,
    LoginForm,
    RequestResetForm,
    ResetPasswordForm
)
from app.models.user import User
from werkzeug.security import generate_password_hash
from app.extensions import mongo, mail
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_mail import Message


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    A basic registration route that:
      - Collects first_name (and optionally last_name), email, and password.
      - Inserts a new user document in MongoDB.
      - Redirects to the login page on success.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegistrationForm()
    if form.validate_on_submit():  # or if request.method == "POST" if no validators
        # Hash the password
        hashed_pw = generate_password_hash(form.password.data)
        new_user = {
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,   # if you capture this in the form
            "email": form.email.data.lower(),
            "password_hash": hashed_pw,
        }
        # Insert user into Mongo
        mongo.db.users.insert_one(new_user)

        flash("Registration successful! You can now log in.", "success")
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

        # Security measure: do not reveal if the email doesn't exist
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
        # Token stores the user's email (or user ID).
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

    # Use 'first_name' instead of 'username'. If your model stores first_name, do user_obj.first_name.
    # If last_name is optional, you can combine them or just use first_name alone.
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