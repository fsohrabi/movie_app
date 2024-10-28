from app import db
from app.models.movie import Movie
from app.models.user import User


class Review(db.Model):
    """Model representing a movie review."""

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    movie_id = db.Column(db.Integer, db.ForeignKey(Movie.id))
    rating = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Review(id={self.id}, text='{self.text}')>"

    def __str__(self):
        return f"Review: {self.text}"
