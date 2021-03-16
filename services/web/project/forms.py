"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
import email_validator
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional
)


class SignupForm(FlaskForm):
    """Sponsor Type User Sign-up Form."""
    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password.')
        ]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    organization = StringField(
        'Organization',
        validators=[Optional()]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')



class NewDocumentForm(FlaskForm):
    """Create New Document Form."""
    document_name = StringField(
        'Document Name',
        validators=[Optional()]
    )
    document_body = StringField(
        'Document Body',
        validators=[Optional()]
    )
    submit = SubmitField('Submit')


class PastebinEntry(FlaskForm):
    language = SelectField(
        u'Programming Language', 
        choices=[('cpp', 'C++'), 
        ('py', 'Python'), 
        ('text', 'Plain Text')]
        )