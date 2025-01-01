# app/blueprints/user/routes.py

from bson import ObjectId
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import user_bp
from .forms import RegistrationForm, ViewProfileForm, EditProfileForm
from ...extensions import mongo
# Instead of 'create_user_and_assign_account', we import the multi-account function:
from app.blueprints.services.user_service import create_user_with_account_option


@user_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    A route for user registration that populates a dropdown of existing accounts
    or allows the user to choose 'NEW', which creates a new account doc.
    """

    form = RegistrationForm()

    # 1. Get existing accounts from DB
    accounts_list = mongo.db.accounts.find({})  # or some filter if needed

    # 2. Build choices: e.g. [("NEW", "Create New Account"), ("64fdbb...", "Acme Corp"), ...]
    account_choices = [("NEW", "Create New Account")]  # default special choice
    for acct in accounts_list:
        # Use acct["account_name"] if you store a name, or fallback to str(_id)
        label = acct.get("account_name", str(acct["_id"]))
        account_choices.append((str(acct["_id"]), label))

    # 3. Assign these to the form’s existing_acct_id choices
    form.existing_acct_id.choices = account_choices

    # 4. On form submit, handle user creation
    if form.validate_on_submit():
        # Grab the user’s chosen ID (or "NEW")
        existing_acct_choice = form.existing_acct_id.data

        new_user_id = create_user_with_account_option(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data,
            existing_acct_id=existing_acct_choice
        )

        flash("User registered!", "success")
        return redirect(url_for("user.login"))

    return render_template("user/register.html", form=form)


@user_bp.route('/profile', methods=['GET'])
@login_required
def view_profile():
    """
    Displays the currently logged-in user's profile in read-only mode.
    Re-queries Mongo to ensure we have the latest data, rather than relying
    on the potentially stale session object in current_user.
    """
    user_id = current_user.get_id()
    user_doc = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user_doc:
        flash("User not found in the database.", "danger")
        return redirect(url_for("main.dashboard"))

    # Populate a read-only form (no validators, purely for display)
    form = ViewProfileForm()
    form.email.data      = user_doc.get("email", "")
    form.first_name.data = user_doc.get("first_name", "")
    form.last_name.data  = user_doc.get("last_name", "")
    form.phone.data      = user_doc.get("phone", "")
    form.time_zone.data  = user_doc.get("time_zone", "")
    form.about_me.data   = user_doc.get("about_me", "")

    return render_template("user/view_profile.html", user=user_doc, form=form)


@user_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Allows the currently logged-in user to update their profile details.
    Re-queries Mongo for the user's document and updates fields on POST.
    """
    user_id = current_user.get_id()
    user_doc = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user_doc:
        flash("User not found in the database.", "danger")
        return redirect(url_for("main.dashboard"))

    form = EditProfileForm()

    if request.method == "GET":
        # Pre-populate the form fields with what's in Mongo
        form.email.data      = user_doc.get("email", "")
        form.first_name.data = user_doc.get("first_name", "")
        form.last_name.data  = user_doc.get("last_name", "")
        form.phone.data      = user_doc.get("phone", "")
        form.time_zone.data  = user_doc.get("time_zone", "")
        form.about_me.data   = user_doc.get("about_me", "")

    elif form.validate_on_submit():
        updated_fields = {
            "email":      form.email.data,
            "first_name": form.first_name.data,
            "last_name":  form.last_name.data,
            "phone":      form.phone.data,
            "time_zone":  form.time_zone.data,
            "about_me":   form.about_me.data,
        }

        result = mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": updated_fields})

        if result.modified_count > 0:
            flash("Profile updated successfully!", "success")
        else:
            flash("No changes made or user not found.", "warning")

        return redirect(url_for("user.view_profile"))
    else:
        flash("Please correct the errors below.", "danger")

    return render_template("user/edit_profile.html", form=form, user=user_doc)