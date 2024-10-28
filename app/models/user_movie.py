from app import db
from app.models.movie import Movie
from app.models.user import User


class UserMovie(db.Model):
    """Model representing the relationship between users and movies."""

    __tablename__ = 'user_movies'

    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete="CASCADE"), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(Movie.id, ondelete="CASCADE"), primary_key=True)
    watched_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<UserMovie(user_id={self.user_id}, movie_id='{self.movie_id}')>"
