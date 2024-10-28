from flask import Blueprint, render_template

# Define a blueprint for the main routes
main_routes = Blueprint('main_routes', __name__)


@main_routes.route('/', methods=['GET', 'POST'])
def home():
    """Render the home page.

    This function handles GET and POST requests for the home page
    and renders the 'index.html' template.
    """
    return render_template('index.html')


@main_routes.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors.

    This function is called when a requested resource is not found.
    It renders the '404.html' template and returns a 404 status code.

    Args:
        e: The error object.

    Returns:
        A tuple containing the rendered template and the 404 status code.
    """
    return render_template('404.html'), 404


@main_routes.errorhandler(403)
def forbidden(e):
    """Handle 403 errors.

    This function is called when access to a resource is forbidden.
    It renders the '403.html' template and returns a 403 status code.

    Args:
        e: The error object.

    Returns:
        A tuple containing the rendered template and the 403 status code.
    """
    return render_template('403.html'), 403
