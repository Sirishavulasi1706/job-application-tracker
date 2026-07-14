from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

login_manager.login_view = "auth.login"


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.dashboard import dashboard
    from app.routes.applications import applications
    from app.routes.resume import resume
    from app.routes.job_match import job_match
    from app.routes.history import history

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(applications)
    app.register_blueprint(resume)
    app.register_blueprint(job_match)
    app.register_blueprint(history)

    from app import models

    return app