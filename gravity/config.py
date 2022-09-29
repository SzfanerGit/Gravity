import os


class Config:
    SECRET_KEY = '8aabed13502bfd634e0f338428fe0e59'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///gravity.db'

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # TODO try to figure out why os.environ makes problems with logging in
    MAIL_USERNAME = os.environ.get('GRAVITY_EMAIL')
    MAIL_PASSWORD = os.environ.get('GRAVITY_EMAIL_PASSWORD')