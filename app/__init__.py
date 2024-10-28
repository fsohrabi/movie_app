from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import config
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[env])

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Move the imports here
    from app.models.movie import Movie
    from app.models.user import User
    from app.models.user_movie import UserMovie

    from app.routes.main import main_routes
    app.register_blueprint(main_routes)
    from app.routes.admin import admin_routes
    app.register_blueprint(admin_routes)
    from app.routes.users import user_routes
    app.register_blueprint(user_routes)
    from app.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.datamanager.sqlite_data_manager import SQLiteDataManager
        data_manager = SQLiteDataManager(db)
        return data_manager.get_user_by_id(user_id)

    return app
