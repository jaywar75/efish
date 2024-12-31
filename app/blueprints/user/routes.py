# app/blueprints/user/routes.py

from bson import ObjectId
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import user_bp
from .forms import ViewProfileForm, EditProfileForm
from ...extensions import mongo  # Adjust import path if your 'extensions' location differs


@user_bp.route('/profile', methods=['GET'])
@login_required
def view_profile():
    """
    Displays the currently logged-in user's profile in read-only mode.
    We re-query Mongo to ensure we have the latest data, rather than relying
    on the potentially stale session object in current_user.
    """
    user_id = current_user.get_id()  # or current_user._id if that's how you store it
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

    # Pass the fresh user_doc & form to the template
    return render_template(
        "user/view_profile.html",
        user=user_doc,
        form=form
    )


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
        # Collect updated data from the form
        updated_fields = {
            "email":      form.email.data,
            "first_name": form.first_name.data,
            "last_name":  form.last_name.data,
            "phone":      form.phone.data,
            "time_zone":  form.time_zone.data,
            "about_me":   form.about_me.data,
        }

        # Update in Mongo
        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": updated_fields}
        )

        if result.modified_count > 0:
            flash("Profile updated successfully!", "success")
        else:
            # Possibly the user made no changes, or the user was not found
            flash("No changes made or user not found.", "warning")

        return redirect(url_for("user.view_profile"))
    else:
        # If POST but form validation failed:
        flash("Please correct the errors below.", "danger")

    # Render the template with the form (and optionally user_doc)
    return render_template(
        "user/edit_profile.html",
        form=form,
        user=user_doc
    )