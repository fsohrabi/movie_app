from app import db


class Movie(db.Model):
    """Model representing a movie."""

    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    director = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=True)

    genres = db.relationship(
        'Genre',
        secondary='movie_genres',
        backref=db.backref('movies', lazy='dynamic'),
        cascade="save-update, merge"
    )
    reviews = db.relationship(
        'Review',
        backref='movies',
        lazy=True,
        cascade="all, delete-orphan"
    )
    user_movies = db.relationship(
        'UserMovie',
        backref='movies',
        cascade="all, delete-orphan",
        lazy=True,
    )

    def __repr__(self):
        return f"<Movie(id={self.id}, name='{self.name}')>"

    def __str__(self):
        return f"Movie: {self.name}"
