import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from dotenv import load_dotenv


load_dotenv()


class SignupForm(FlaskForm):
    """
    Form for user signup with fields for name, email, and password.
    Validates the uniqueness of the email against a predefined admin email.

    Attributes:
        name (StringField): The name of the user.
        email (StringField): The email address of the user.
        password (PasswordField): The user's password.
        submit (SubmitField): The button to submit the form.
    """

    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        """
        Validate that the email is not the admin email.

        Args:
            email (StringField): The email field to validate.

        Raises:
            ValidationError: If the email matches the admin email.
        """
        admin_email = os.getenv('ADMIN_EMAIL')
        if email.data == admin_email:
            raise ValidationError('You cannot register with this email.')
