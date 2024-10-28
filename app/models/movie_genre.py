from app import db
from app.models.movie import Movie
from app.models.genre import Genre


class MovieGenre(db.Model):
    __tablename__ = 'movie_genres'

    # Define the two foreign keys and set them as a composite primary key
    genre_id = db.Column(db.Integer, db.ForeignKey(Genre.id, ondelete="CASCADE"), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(Movie.id, ondelete="CASCADE"), primary_key=True)

    def __repr__(self):
        """
        Returns a string representation of the MovieGenre instance for debugging purposes.

        Returns:
            str: The representation of the MovieGenre object.
        """
        return f"<MovieGenre(genre_id={self.user_id}, movie_id='{self.movie_id}')>"
