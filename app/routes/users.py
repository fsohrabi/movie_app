from flask import Blueprint, request, render_template, url_for, flash, redirect, abort
from app import db
from app.datamanager.sqlite_data_manager import SQLiteDataManager
from flask_login import current_user, login_required
import logging
from app.forms.movie_form import MovieForm
from app.forms.review_form import ReviewForm

logging.basicConfig(level=logging.DEBUG)

# Initialize the data manager
data_manager = SQLiteDataManager(db)

# Define a blueprint for user routes
user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/user/movies', methods=['GET'])
@login_required
def get_user_movies():
    """Render the user's movies page.

    Fetches and displays the movies associated with the current user.

    Returns:
        Rendered template with the user's movies.
    """
    user_movies = data_manager.get_user_movies(user_id=current_user.id)
    logging.debug(f"User Movies: {user_movies}")  # Use logging instead of print
    return render_template('movies.html', user_movies=user_movies)


@user_routes.route('/user/movies/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    form = MovieForm()
    genres = [(genre.id, genre.name) for genre in data_manager.get_all_genre()]
    form.genres.choices = genres
    if form.validate_on_submit():
        try:
            new_movie = data_manager.add_movie(
                name=form.name.data,
                director=form.director.data,
                year=form.year.data,
                rating=form.rating.data,
            )
            selected_genres = data_manager.get_genres_by_ids(form.genres.data)
            new_movie.genres.extend(selected_genres)
            data_manager.add_user_movie(user_id=current_user.id, movie_id=new_movie.id)
            flash(f'Movie "{new_movie.name}" added successfully!', 'success')
            return redirect(url_for('user_routes.get_user_movies'))
        except Exception as e:
            logging.error("Error adding movie: %s", str(e))
            flash('An error occurred while adding the movie.', 'danger')

    genres = data_manager.get_all_genre()
    return render_template('add_movie.html', form=form, genres=genres)


@user_routes.route('/user/movies/update_movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def update_movie(movie_id):
    """Update an existing movie's details.

    This route handles both displaying the current movie details and processing updates.

    Args:
        movie_id: The ID of the movie to be updated.

    Returns:
        Rendered template for updating the movie or redirects to the user's movies page.
    """
    movie = get_movie_or_abort(movie_id)
    form = MovieForm()
    if request.method == 'POST':
        form.genres.choices = [(genre.id, genre.name) for genre in data_manager.get_all_genre()]  # Set choices
        movie = get_movie_or_abort(movie_id)
        if form.validate_on_submit():
            try:
                movie.title = request.form.get('title')
                movie.director = request.form.get('director')
                movie.year = request.form.get('year')
                movie.rating = request.form.get('rating')
                genre_ids = request.form.getlist('genres')
                selected_genre_ids = set(genre_ids)
                current_genre_ids = {genre.id for genre in movie.genres}
                genres_to_remove = current_genre_ids - selected_genre_ids
                for genre_id in genres_to_remove:
                    data_manager.delete_movie_genre(movie.id, genre_id)
                genres_to_add = selected_genre_ids - current_genre_ids
                for genre_id in genres_to_add:
                    genre = data_manager.get_genre_by_id(genre_id)
                    if genre:
                        movie.genres.append(genre)

                db.session.commit()  # Commit the changes
                flash('Movie updated successfully!', 'success')
                return redirect(url_for('user_routes.get_user_movies'))
            except Exception as e:
                logging.error("Error update movie: %s", str(e))
                flash('An error occurred while update the movie.', 'danger')
    else:
        form.name.data = movie.name
        form.director.data = movie.director
        form.year.data = movie.year
        form.rating.data = movie.rating
        form.genres.data = [str(genre.id) for genre in movie.genres]
        genres = data_manager.get_all_genre()
        return render_template('update_movie.html',form=form, movie=movie, genres=genres)


@user_routes.route('/user/movies/<int:movie_id>/delete', methods=['POST'])
@login_required
def delete_movie(movie_id):
    """Delete a movie associated with the logged-in user.

    Args:
        movie_id: The ID of the movie to be deleted.

    Returns:
        Redirects to the user's movies page.
    """
    movie = data_manager.get_movie_by_id(movie_id, current_user.id)
    if movie:  # Ensure user can only delete their own movies
        data_manager.delete_movie(movie_id)
        flash('Movie deleted successfully!', 'success')
    else:
        flash('Unauthorized action!', 'danger')
    return redirect(url_for('user_routes.get_user_movies'))


@user_routes.route('/user/movies/show_movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def show_movie(movie_id):
    """Display the details of a specific movie along with user reviews.

    Args:
        movie_id: The ID of the movie to display.

    Returns:
        Rendered template for displaying movie details and reviews.
    """
    movie = get_movie_or_abort(movie_id)
    user_reviews = data_manager.get_user_reviews_for_movie(movie_id=movie_id, user_id=current_user.id)
    form = ReviewForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data_manager.add_user_review(
                movie_id=movie_id,
                user_id=current_user.id,
                text=form.review.data,
                rating=form.rating.data
            )
        flash('Review added successfully!', 'success')
        return redirect(url_for('user_routes.show_movie', movie_id=movie_id))

    # Render the movie detail page
    return render_template('show_movie.html', movie=movie, user_reviews=user_reviews,form=form)


@user_routes.route('/user/reviews/<int:review_id>/delete', methods=['POST'])
@login_required
def delete_review(review_id):
    """Delete a specific review created by the logged-in user.

    Args:
        review_id: The ID of the review to be deleted.

    Returns:
        Redirects to the movie details page.
    """
    review = data_manager.get_review_by_id(review_id)
    if review and review.user_id == current_user.id:  # Ensure user can only delete their own reviews
        data_manager.delete_review(review_id)
        flash('Review deleted successfully!', 'success')
    else:
        flash('Unauthorized action!', 'danger')

    return redirect(url_for('user_routes.show_movie', movie_id=review.movie_id))


def get_movie_or_abort(movie_id):
    movie = data_manager.get_movie_by_id(movie_id, current_user.id)
    if movie is None:
        abort(403)
    return movie
