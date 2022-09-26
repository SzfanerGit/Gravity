import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = '8aabed13502bfd634e0f338428fe0e59'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gravity.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# TODO try to figure out why os.environ makes problems with logging in
app.config['MAIL_USERNAME'] = 'gravity.project.app@gmail.com'
app.config['MAIL_PASSWORD'] = 'daodjadsdqexydjf'
mail = Mail(app)

# what do I need it for? TODO check
from gravity import routes