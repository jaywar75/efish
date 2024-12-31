# app/blueprints/user/routes.py

from bson import ObjectId
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import user_bp
from .forms import EditProfileForm, ViewProfileForm
from ...extensions import mongo


@user_bp.route('/profile', methods=['GET'])
@login_required
def view_profile():
    """
    Display the logged-in user's profile page.
    If needed, you can fetch fresh data from Mongo.
    But if current_user is already loaded from DB on each request,
    you can simply rely on it.

    Example of using a ViewProfileForm if you want
    to show read-only fields or gather minimal input.
    """
    form = ViewProfileForm(obj=current_user)

    # Typically, on a GET request, we wouldn’t do form.validate_on_submit().
    # But if you had a button on the profile page that posts data
    # (e.g. "Change Avatar" or something), you could handle it here.
    # For now, we’ll just ignore form POST logic since the route is GET only.

    return render_template('user/view_profile.html', user=current_user, form=form)


@user_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Let the user update their profile details.
    We'll store them in the same 'users' collection that auth uses.
    """
    form = EditProfileForm(obj=current_user)

    if form.validate_on_submit():
        # 1) Gather form data
        #    (Your EditProfileForm might have fields: first_name, last_name, phone, about_me, etc.)
        updated_fields = {
            "email":      form.email.data,
            "first_name": request.form.get('first_name', ''),
            "last_name":  request.form.get('last_name', ''),
            "phone":      request.form.get('phone', ''),
            "time_zone":  request.form.get('time_zone', ''),
            "about_me":   request.form.get('about_me', ''),
        }

        # 2) Convert current_user’s ID to ObjectId if necessary
        user_id = current_user.get_id()  # or current_user._id if that’s how you store it

        # 3) Update the user document in Mongo
        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": updated_fields}
        )

        # 4) Check result and flash a message
        if result.modified_count > 0:
            flash("Profile updated successfully!", "success")
        else:
            # Possibly means no changes were made or user_id wasn't found
            flash("No changes or user not found.", "warning")

        # Redirect to profile page
        return redirect(url_for('user.view_profile'))

    # On GET or if form fails validation, show the edit form
    return render_template('user/edit_profile.html', form=form, user=current_user)