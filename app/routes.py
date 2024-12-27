# app/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .forms import LoginForm, RegistrationForm
from . import mongo, login_manager

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.users.find_one({'_id': mongo.db.ObjectId(user_id)})
    if user:
        return User(user)
    return None

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({'email': form.email.data})
        if user and check_password_hash(user['password_hash'], form.password.data):
            user_obj = User(user)
            login_user(user_obj, remember=form.remember.data)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.home'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = mongo.db.users.find_one({'email': form.email.data})
        if existing_user:
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

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))