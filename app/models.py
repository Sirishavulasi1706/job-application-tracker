from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    applications = db.relationship(
        "JobApplication",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )


class JobApplication(db.Model):

    __tablename__ = "job_applications"

    id = db.Column(db.Integer, primary_key=True)

    company = db.Column(db.String(150), nullable=False)

    role = db.Column(db.String(150), nullable=False)

    location = db.Column(db.String(100))

    status = db.Column(db.String(50), default="Applied")

    job_link = db.Column(db.String(500))

    notes = db.Column(db.Text)

    applied_date = db.Column(db.Date)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )


class ResumeAnalysis(db.Model):

    __tablename__ = "resume_analyses"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    resume_filename = db.Column(
        db.String(255),
        nullable=False
    )

    analysis = db.Column(
        db.Text,
        nullable=False
    )

    career_insights = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.now()
    )


class InterviewPreparation(db.Model):

    __tablename__ = "interview_preparations"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    application_id = db.Column(
        db.Integer,
        db.ForeignKey("job_applications.id"),
        nullable=False
    )

    questions = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.now()
    )


class ResumeOptimization(db.Model):

    __tablename__ = "resume_optimizations"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    resume_analysis_id = db.Column(
        db.Integer,
        db.ForeignKey("resume_analyses.id"),
        nullable=False
    )

    job_description = db.Column(
        db.Text,
        nullable=False
    )

    optimization = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.now()
    )