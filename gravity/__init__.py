from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from gravity.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'warning'

mail = Mail()


def create_app(config_class=Config):
    # Configure application
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Get pages
    from gravity.main.routes import main
    from gravity.users.routes import users
    app.register_blueprint(main)
    app.register_blueprint(users)

    return app