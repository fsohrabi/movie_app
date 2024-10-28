from flask_sqlalchemy import SQLAlchemy
from abc import ABC
from app.datamanager.data_manager_interface import DataManagerInterface
from app.models.user import User
from app.models.movie import Movie
from app.models.user_movie import UserMovie
from app.models.genre import Genre
from app.models.review import Review
from app.models.movie_genre import MovieGenre


class SQLiteDataManager(DataManagerInterface, ABC):
    """Data manager for interacting with SQLite database models."""

    def __init__(self, db: SQLAlchemy):
        """Initialize SQLiteDataManager with a SQLAlchemy database session."""
        self.db = db

    def get_all_users(self):
        """Retrieve all users from the database."""
        return self.db.session.query(User).all()

    def get_user_movies(self, user_id: int):
        """Retrieve all movies associated with a specific user."""
        return (self.db.session.query(Movie)
                .join(UserMovie)
                .filter(UserMovie.user_id == user_id)
                .all())

    def add_user(self, name: str, email: str, password: str):
        """Add a new user to the database with the provided name, email, and password."""
        user = User(name=name, email=email, password=password)
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def get_user_by_email(self, email: str):
        """Retrieve a user by their email address."""
        return self.db.session.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: int):
        """Retrieve a user by their unique ID."""
        return self.db.session.query(User).filter(User.id == user_id).first()

    def delete_user(self, user_id: int):
        """Delete a user and associated data by their unique ID."""
        user = self.get_user_by_id(user_id)
        if user:
            self.db.session.delete(user)
            self.db.session.commit()

    def add_movie(self, name: str, director: str, year: int, rating: float):
        """Add a new movie to the database with specified details."""
        movie = Movie(name=name, director=director, year=year, rating=rating)
        self.db.session.add(movie)
        self.db.session.commit()
        return movie

    def update_movie(self, movie_id: int, title: str, director: str, year: int, rating: float):
        """Update details of an existing movie by its ID."""
        movie = Movie.query.get(movie_id)
        if movie:
            movie.title = title
            movie.director = director
            movie.year = year
            movie.rating = rating
            self.db.session.commit()

    def delete_movie(self, movie_id: int):
        """Delete a movie from the database by its ID."""
        movie = Movie.query.get(movie_id)
        if movie:
            self.db.session.delete(movie)
            self.db.session.commit()

    def get_all_genre(self):
        """Retrieve all genres from the database."""
        return self.db.session.query(Genre).all()

    def get_genres_by_ids(self, ids: list):
        """Retrieve multiple genres by a list of IDs."""
        return self.db.session.query(Genre).filter(Genre.id.in_(ids)).all()

    def add_user_movie(self, user_id: int, movie_id: int):
        """Associate a movie with a user."""
        user_movie = UserMovie(user_id=user_id, movie_id=movie_id)
        self.db.session.add(user_movie)
        self.db.session.commit()

    def add_user_review(self, movie_id: int, user_id: int, text: str, rating: float):
        """Add a review by a user for a specific movie."""
        review = Review(movie_id=movie_id, user_id=user_id, text=text, rating=rating)
        self.db.session.add(review)
        self.db.session.commit()

    def delete_genre(self, genre_id: int):
        """Delete a genre by its ID."""
        genre = Genre.query.get(genre_id)
        if genre:
            self.db.session.delete(genre)
            self.db.session.commit()

    def add_genre(self, name: str, description: str):
        """Add a new genre to the database."""
        genre = Genre(name=name, description=description)
        self.db.session.add(genre)
        self.db.session.commit()

    def get_genres_by_name(self, name: str):
        """Retrieve a genre by its name."""
        return self.db.session.query(Genre).filter(Genre.name == name).first()

    def get_user_reviews_for_movie(self, movie_id: int, user_id: int):
        """Retrieve all reviews a user has made for a specific movie."""
        return (self.db.session.query(Review)
                .filter(Review.movie_id == movie_id, Review.user_id == user_id)
                .all())

    def get_movie_by_id(self, movie_id: int, user_id: int):
        """Retrieve a movie by ID associated with a specific user."""
        return (self.db.session.query(Movie)
                .join(UserMovie)
                .filter(Movie.id == movie_id, UserMovie.user_id == user_id)
                .first())

    def delete_review(self, review_id: int):
        """Delete a review by its ID."""
        review = Review.query.get(review_id)
        if review:
            self.db.session.delete(review)
            self.db.session.commit()

    def delete_movie_genre(self, movie_id: int, genre_id: int):
        """Remove association between a movie and a genre by their IDs."""
        movie_genre = (self.db.session.query(MovieGenre)
                       .filter(MovieGenre.movie_id == movie_id, MovieGenre.genre_id == genre_id)
                       .first())
        if movie_genre:
            self.db.session.delete(movie_genre)
            self.db.session.commit()

    def get_review_by_id(self, review_id: int):
        """Retrieve a review by its unique ID."""
        return self.db.session.query(Review).filter(Review.id == review_id).first()

    def get_genre_by_id(self, genre_id: int):
        """Retrieve a genre by its unique ID."""
        return self.db.session.query(Genre).filter(Genre.id == genre_id).first()
