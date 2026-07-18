
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app.models import JobApplication, InterviewPreparation
from app import db
from app.ai.interview_generator import generate_interview_questions

interview = Blueprint("interview", __name__)


@interview.route("/interview", methods=["GET", "POST"])
@login_required
def interview_home():

    applications = JobApplication.query.filter_by(
        user_id=current_user.id
    ).all()

    questions = None

    if request.method == "POST":

        application_id = request.form.get("application")

        application = JobApplication.query.filter_by(
            id=application_id,
            user_id=current_user.id
        ).first()

        if application:

            saved = InterviewPreparation.query.filter_by(
                user_id=current_user.id,
                application_id=application.id
            ).first()

            if saved:

                questions = saved.questions

            else:

                questions = generate_interview_questions(
                    company=application.company,
                    role=application.role,
                    job_description=application.notes or ""
                )

                new_preparation = InterviewPreparation(
                    user_id=current_user.id,
                    application_id=application.id,
                    questions=questions
                )

                db.session.add(new_preparation)
                db.session.commit()

    history = (
        InterviewPreparation.query
        .filter_by(user_id=current_user.id)
        .order_by(InterviewPreparation.created_at.desc())
        .all()
    )

    return render_template(
        "interview.html",
        applications=applications,
        questions=questions,
        history=history
    )

