from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectMultipleField, FloatField, SubmitField
from wtforms.validators import DataRequired


class MovieForm(FlaskForm):
    """Form for adding or updating movie details."""

    name = StringField('Name', validators=[DataRequired()])
    director = StringField('Director', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    rating = FloatField('Rating', validators=[DataRequired()])
    genres = SelectMultipleField('Genres', coerce=int)
    submit = SubmitField('Submit')
