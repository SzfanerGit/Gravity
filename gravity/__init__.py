from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = '8aabed13502bfd634e0f338428fe0e59'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gravity.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'

# what do I need it for? TODO check
from gravity import routes