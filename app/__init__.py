from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from config import Config
from app.scheduler.reminder_scheduler import start_scheduler

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()

login_manager.login_view = "auth.login"


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.dashboard import dashboard
    from app.routes.applications import applications
    from app.routes.resume import resume
    from app.routes.job_match import job_match
    from app.routes.history import history
    from app.routes.interview import interview
    from app.routes.resume_optimizer import resume_optimizer
    from app.routes.reminders import reminders
    from app.routes.cover_letter import cover_letter
    from app.routes.resume_builder import resume_builder
    from app.routes.career_chat import career_chat

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(applications)
    app.register_blueprint(resume)
    app.register_blueprint(job_match)
    app.register_blueprint(history)
    app.register_blueprint(interview)
    app.register_blueprint(resume_optimizer)
    app.register_blueprint(reminders)
    app.register_blueprint(cover_letter)
    app.register_blueprint(resume_builder)
    app.register_blueprint(career_chat)

    from app import models

    start_scheduler(app)


    @app.errorhandler(404)
    def page_not_found(error):
        return render_template(
            "errors/404.html"
        ), 404


    @app.errorhandler(500)
    def internal_server_error(error):
        db.session.rollback()
        return render_template(
            "errors/500.html"
        ), 500


    return app