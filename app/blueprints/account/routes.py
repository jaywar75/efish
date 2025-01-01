# app/blueprints/account/routes.py

from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request
)
from flask_login import login_required
from bson.objectid import ObjectId

from . import account_bp
from ...extensions import mongo
from .forms import EditAccountForm  # or wherever EditAccountForm is defined


@account_bp.route("/view/<account_id>", methods=["GET"])
@login_required
def view_account(account_id):
    """
    Displays the specified account's details in read-only format.
    If not found, flashes an error and redirects to the main dashboard.
    """
    account_doc = mongo.db.accounts.find_one({"_id": ObjectId(account_id)})
    if not account_doc:
        flash("Account not found.", "danger")
        return redirect(url_for("main.dashboard"))

    return render_template("view_account.html", account=account_doc)


@account_bp.route("/edit/<account_id>", methods=["GET", "POST"])
@login_required
def edit_account(account_id):
    """
    Allows editing of an account's 'account_name' and 'plan_type'.
    If the account doesn't exist, flashes an error and redirects.
    On POST, updates the doc in Mongo and redirects back to 'view_account'.
    """
    account_doc = mongo.db.accounts.find_one({"_id": ObjectId(account_id)})
    if not account_doc:
        flash("Account not found", "danger")
        return redirect(url_for("main.dashboard"))

    form = EditAccountForm()

    if request.method == "GET":
        # Pre-populate the form fields with what's in Mongo
        form.account_name.data = account_doc.get("account_name", "")
        form.plan_type.data = account_doc.get("plan_type", "")
    elif form.validate_on_submit():
        # Gather updated data from the form
        updated_data = {
            "account_name": form.account_name.data,
            "plan_type": form.plan_type.data
        }
        mongo.db.accounts.update_one(
            {"_id": account_doc["_id"]},
            {"$set": updated_data}
        )
        flash("Account updated!", "success")
        return redirect(url_for("account.view_account", account_id=account_id))
    else:
        # If POST but the form doesn't validate (or there's no validation),
        # show an error message and let the user correct any mistakes.
        flash("Please correct any errors below.", "danger")

    return render_template(
        "edit_account.html",
        form=form,
        account=account_doc
    )