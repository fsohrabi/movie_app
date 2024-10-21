from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        """
        Returns a string representation of the User instance for debugging purposes.

        Returns:
            str: The representation of the User object.
        """
        return f"<User(id={self.id}, name='{self.name}')>"

    def __str__(self):
        """
        Returns a human-readable string representation of the user instance.

        Returns:
            str: A string with the user's name.
        """
        return f"Author: {self.name}"
