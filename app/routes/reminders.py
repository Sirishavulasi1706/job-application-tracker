
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.forms import InterviewReminderForm
from app.models import JobApplication, InterviewReminder

reminders = Blueprint("reminders", __name__)


@reminders.route("/reminders", methods=["GET", "POST"])
@login_required
def schedule_interview():

    form = InterviewReminderForm()

    applications = JobApplication.query.filter_by(
        user_id=current_user.id
    ).all()

    form.application.choices = [
        (
            app.id,
            f"{app.company} - {app.role}"
        )
        for app in applications
    ]

    if form.validate_on_submit():

        reminder = InterviewReminder(
            user_id=current_user.id,
            application_id=form.application.data,
            interview_date=form.interview_date.data,
            interview_time=form.interview_time.data
        )

        db.session.add(reminder)
        db.session.commit()

        flash(
            "Interview scheduled successfully!",
            "success"
        )

        return redirect(
            url_for("reminders.schedule_interview")
        )

    reminders_list = (
        InterviewReminder.query
        .filter_by(user_id=current_user.id)
        .order_by(
            InterviewReminder.interview_date
        )
        .all()
    )

    return render_template(
        "reminders.html",
        form=form,
        reminders=reminders_list
    )

