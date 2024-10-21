from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    director = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=True)

    def __repr__(self):
        """
        Returns a string representation of the Movie instance for debugging purposes.

        Returns:
            str: The representation of the movie object.
        """
        return f"<Movie(id={self.id}, name='{self.name}')>"

    def __str__(self):
        """
        Returns a human-readable string representation of the Movie instance.

        Returns:
            str: A string with the movie's name.
        """
        return f"Author: {self.name}"