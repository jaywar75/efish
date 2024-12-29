# app/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .forms import LoginForm, RegistrationForm
from . import mongo, login_manager
from datetime import datetime

# Define the Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def home():
    """
        Home route displaying the dashboard with the total number of tasks
        and the five most recent tasks for the current user.
        """
    # Fetch the total number of tasks for the current user
    total_tasks = mongo.db.tasks.count_documents({'user_id': current_user.id})

    # Fetch the five most recent tasks, sorted by creation date in descending order
    recent_tasks = list(
        mongo.db.tasks.find({'user_id': current_user.id})
                        .sort('created_at', -1)
                        .limit(5)
    )

    # Optional: Convert 'created_at' to a Python datetime object if it's not already
    for task in recent_tasks:
        if isinstance(task.get('created_at'), str):
            task['created_at'] = datetime.strptime(task['created_at'], '%Y-%m-%dT%H:%M:%SZ')

    return render_template('home.html', total_tasks=total_tasks, recent_tasks=recent_tasks)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Authenticate using username
        user_data = mongo.db.users.find_one({'username': form.username.data})
        if user_data and check_password_hash(user_data['password_hash'], form.password.data):
            user = User(user_data)
            login_user(user, remember=form.remember.data)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.home'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username already exists
        existing_username = mongo.db.users.find_one({'username': form.username.data})
        if existing_username:
            flash('Username already taken. Please choose a different one.', 'warning')
            return redirect(url_for('main.register'))

        # Check if email already exists
        existing_email = mongo.db.users.find_one({'email': form.email.data})
        if existing_email:
            flash('Email already registered.', 'warning')
            return redirect(url_for('main.register'))

        hashed_password = generate_password_hash(form.password.data)
        user_id = mongo.db.users.insert_one({
            'username': form.username.data,
            'email': form.email.data,
            'password_hash': hashed_password
        }).inserted_id
        user = mongo.db.users.find_one({'_id': user_id})
        user_obj = User(user)
        login_user(user_obj)
        flash('Registration successful!', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', form=form)

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))