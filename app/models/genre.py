from app import db


class Genre(db.Model):
    """Model representing a genre of a movie."""

    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Genre(id={self.id}, name='{self.name}')>"

    def __str__(self):
        return f"Genre: {self.name}"
