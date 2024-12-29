# app/routes.py

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from bson.objectid import ObjectId

from . import main_bp
from .forms import LoginForm
from .models import User
from .extensions import mongo, login_manager

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    form = LoginForm()
    if form.validate_on_submit():
        # Fetch user from MongoDB
        user_data = mongo.db.users.find_one({'username': form.username.data})
        if user_data and check_password_hash(user_data['password'], form.password.data):
            user = User(user_data)
            login_user(user)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('tasks.list_tasks'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@main_bp.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))