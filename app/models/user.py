from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from sqlalchemy import event
from app.models.movie import Movie

from app import db


class User(db.Model, UserMixin):
    """Model representing a user."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100))
    user_movies = db.relationship(
        'UserMovie',
        backref='users',
        cascade="all, delete-orphan",
        lazy=True
    )
    reviews = db.relationship(
        'Review',
        backref='users',
        cascade="all, delete-orphan",
        lazy=True
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.email == 'admin@admin.com'

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"

    def __str__(self):
        return f"User: {self.name}"


@event.listens_for(User, 'after_delete')
def cleanup_movies(mapper, connection, target):
    # Access the current session directly from the connection context
    session = db.session.object_session(target)

    # Delete movies that have no associated user_movies
    orphaned_movies = session.query(Movie).filter(~Movie.user_movies.any()).all()
    for movie in orphaned_movies:
        session.delete(movie)



