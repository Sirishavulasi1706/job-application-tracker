from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except Exception:
        return None



class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    email_verified = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    verification_token = db.Column(
        db.String(255),
        unique=True
    )

    applications = db.relationship(
        "JobApplication",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    reminders = db.relationship(
        "InterviewReminder",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # ----------------------------
    # Password Reset
    # ----------------------------

    def get_reset_token(self):
        from app.services.email_service import generate_reset_token
        return generate_reset_token(self.email)

    @staticmethod
    def verify_reset_token(token):
        from app.services.email_service import verify_reset_token
        return verify_reset_token(token)


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

    reminders = db.relationship(
        "InterviewReminder",
        backref="application",
        lazy=True,
        cascade="all, delete-orphan"
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


class InterviewReminder(db.Model):

    __tablename__ = "interview_reminders"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

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

    interview_date = db.Column(
        db.Date,
        nullable=False
    )

    interview_time = db.Column(
        db.Time,
        nullable=False
    )

    reminder_sent = db.Column(
        db.Boolean,
        default=False,
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


class CoverLetter(db.Model):

    __tablename__ = "cover_letters"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    company = db.Column(
        db.String(150),
        nullable=False
    )

    role = db.Column(
        db.String(150),
        nullable=False
    )

    job_description = db.Column(
        db.Text,
        nullable=False
    )

    cover_letter = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.now()
    )


class ResumeBuilder(db.Model):

    __tablename__ = "resume_builders"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    full_name = db.Column(
        db.String(150),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        nullable=False
    )

    phone = db.Column(
        db.String(50)
    )

    linkedin = db.Column(
        db.String(255)
    )

    github = db.Column(
        db.String(255)
    )

    portfolio = db.Column(
        db.String(255)
    )

    education = db.Column(
        db.Text,
        nullable=False
    )

    skills = db.Column(
        db.Text,
        nullable=False
    )

    experience = db.Column(
        db.Text
    )

    projects = db.Column(
        db.Text
    )

    certifications = db.Column(
        db.Text
    )

    achievements = db.Column(
        db.Text
    )

    generated_resume = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.now()
    )


class CareerChat(db.Model):

    __tablename__ = "career_chats"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    user_message = db.Column(
        db.Text,
        nullable=False
    )

    ai_response = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.now()
    )