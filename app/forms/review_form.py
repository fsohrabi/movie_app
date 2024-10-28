from flask_wtf import FlaskForm
from wtforms import TextAreaField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class ReviewForm(FlaskForm):
    """Form for submitting a review and rating for a movie."""

    review = TextAreaField('Review', validators=[DataRequired()])
    rating = FloatField('Rating', validators=[DataRequired(), NumberRange(min=0, max=10)])
    submit = SubmitField('Submit')
