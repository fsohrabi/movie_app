import logging
import os
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.datamanager.sqlite_data_manager import SQLiteDataManager
from app.forms.login_form import LoginForm
from app.forms.signup_form import SignupForm

# Initialize the data manager
data_manager = SQLiteDataManager(db)
logging.basicConfig(level=logging.DEBUG)
auth = Blueprint('auth', __name__)

# Load admin credentials from environment variables
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login, including admin login.

    Validates the login form and checks if the credentials match either
    a normal user or the admin account. If successful, the user is logged
    in and redirected accordingly.
    """
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        logging.debug(f"Form validated. Email: {email}")

        # Check if the user is an admin
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            logging.debug("Admin login detected.")
            session['admin'] = True
            flash('Admin logged in!', 'success')
            return redirect(url_for('admin_routes.admin_dashboard'))

        # Handle normal user login
        user = data_manager.get_user_by_email(email=email)
        if user and check_password_hash(user.password, password):
            login_user(user)
            session['admin'] = False
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main_routes.home'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')
    else:
        logging.debug(f"Form not validated. Errors: {form.errors}")
    return render_template('login.html', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user registration.

    Validates the signup form and registers a new user if the email
    is not already registered. After successful registration, the user
    is logged in and redirected to the home page.
    """
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = data_manager.get_user_by_email(email=form.email.data)
        if existing_user:
            flash('Email is already registered. Please log in.', 'danger')
            return redirect(url_for('auth.login'))

        new_user = data_manager.add_user(
            form.name.data,
            form.email.data,
            generate_password_hash(form.password.data)
        )
        login_user(new_user)
        flash('Registration successful!', 'success')
        return redirect(url_for('main_routes.home'))

    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')

    return render_template('signup.html', form=form)


@auth.route('/logout')
def logout():
    """Log out the current user and clear session data.

    The user is logged out using Flask-Login, and the admin session
    status is cleared. A flash message is shown to indicate the logout
    success.
    """
    logout_user()
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))
