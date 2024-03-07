from flask import Flask
from .config import Config
from flask_login import LoginManager


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Setting up flask login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    with app.app_context():
        from . import routes
        from functions.userclass import User

        @login_manager.user_loader
        def load_user(email):
            return User.get(email)

    return app
