import email
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from gravity.database import User 

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=30,
                           message='Username must be between %(min)d and %(max)d characters long')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up!')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        # if not found in the database then user=None
        if user:
            raise ValidationError('This username is already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        # if not found in the database then user=None
        if user:
            raise ValidationError('This email is already taken.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
     email = StringField('Email', validators=[DataRequired(), Email()])
     submit = SubmitField('Reset Password')

     def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        # if not found in the database then user=None
        if user is None:
            raise ValidationError('There is no account associated with this email address.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')