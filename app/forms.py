from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    SelectField,
    DateField,
    TimeField
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
    URL
)


class RegistrationForm(FlaskForm):

    name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=2, max=100)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    submit = SubmitField("Register")


class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Login")


class ApplicationForm(FlaskForm):

    company = StringField(
        "Company Name",
        validators=[DataRequired()]
    )

    role = StringField(
        "Job Role",
        validators=[DataRequired()]
    )

    location = StringField(
        "Location",
        validators=[Optional()]
    )

    status = SelectField(
        "Application Status",
        choices=[
            ("Applied", "Applied"),
            ("Interview", "Interview"),
            ("Offered", "Offered"),
            ("Rejected", "Rejected")
        ],
        validators=[DataRequired()]
    )

    job_link = StringField(
        "Job Link",
        validators=[Optional(), URL()]
    )

    applied_date = DateField(
        "Applied Date",
        format="%Y-%m-%d",
        validators=[Optional()]
    )

    notes = TextAreaField(
        "Notes",
        validators=[Optional()]
    )

    submit = SubmitField("Save Application")


class JobMatchForm(FlaskForm):

    resume = FileField(
        "Upload Resume",
        validators=[
            FileAllowed(["pdf"], "PDF files only!")
        ]
    )

    job_description = TextAreaField(
        "Job Description",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Analyze Match")


class InterviewReminderForm(FlaskForm):

    application = SelectField(
        "Application",
        coerce=int,
        validators=[DataRequired()]
    )

    interview_date = DateField(
        "Interview Date",
        validators=[DataRequired()]
    )

    interview_time = TimeField(
        "Interview Time",
        validators=[DataRequired()]
    )

    submit = SubmitField(
        "Schedule Interview"
    )


class ForgotPasswordForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    submit = SubmitField(
        "Send Reset Link"
    )


class ResetPasswordForm(FlaskForm):

    password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    submit = SubmitField(
        "Reset Password"
    )