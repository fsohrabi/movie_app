import logging
from functools import wraps
from flask import Blueprint, request, render_template, url_for, flash, redirect, session, abort
from app import db
from app.datamanager.sqlite_data_manager import SQLiteDataManager
from flask_login import current_user

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize the data manager
data_manager = SQLiteDataManager(db)

# Define a blueprint for the admin routes
admin_routes = Blueprint('admin_routes', __name__)


def admin_required(f):
    """Decorator to ensure the user is an admin.

    If the user is not an admin, a 403 Forbidden error is raised.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin'):
            abort(403)  # Forbidden access
        return f(*args, **kwargs)

    return decorated_function


@admin_routes.route('/admin')
@admin_required
def admin_dashboard():
    """Render the admin dashboard.

    Retrieves all users and genres from the database and displays
    the admin_dashboard.html template.
    """
    users = data_manager.get_all_users()
    genres = data_manager.get_all_genre()
    return render_template('admin_dashboard.html', users=users, genres=genres)


@admin_routes.route('/admin/genre/<genre_id>/delete')
@admin_required
def delete_genre(genre_id):
    """Delete a genre by its ID.

    Removes the genre from the database and flashes a success message.
    Redirects to the admin dashboard after deletion.
    """
    data_manager.delete_genre(genre_id)
    flash('Genre is deleted', 'success')
    return redirect(url_for('admin_routes.admin_dashboard'))


@admin_routes.route('/admin/add_genre', methods=['POST'])
@admin_required
def add_genre():
    """Add a new genre to the database.

    Retrieves the genre name and description from the form data,
    checks if the genre already exists, and adds it if not. Flashes
    an appropriate message for the user and redirects to the admin dashboard.
    """
    name = request.form.get('name')
    description = request.form.get('description')
    genre = data_manager.get_genres_by_name(name=name)

    if genre:
        flash('Genre already exists.', 'danger')
    else:
        data_manager.add_genre(name=name, description=description)
        flash('Genre added successfully!', 'success')

    return redirect(url_for('admin_routes.admin_dashboard'))


@admin_routes.route('/admin/delete_user/<int:user_id>', methods=['GET'])
@admin_required
def delete_user(user_id):
    """Delete a user by their ID.

    Removes the user from the database and flashes a success message.
    Redirects to the admin dashboard after deletion.
    """
    data_manager.delete_user(user_id)
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin_routes.admin_dashboard'))
