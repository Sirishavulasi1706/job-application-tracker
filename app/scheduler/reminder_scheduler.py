from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def check_interview_reminders():

    from app import db
    from app.models import InterviewReminder
    from app.services.email_service import send_interview_reminder

    now = datetime.now()

    upcoming = now + timedelta(days=1)

    reminders = InterviewReminder.query.filter_by(
        reminder_sent=False
    ).all()

    for reminder in reminders:

        interview_datetime = datetime.combine(
            reminder.interview_date,
            reminder.interview_time
        )

        if now <= interview_datetime <= upcoming:

            send_interview_reminder(reminder)

            reminder.reminder_sent = True

            db.session.commit()

            print(
                f"Reminder sent for {reminder.application.company}"
            )


def start_scheduler(app):

    if scheduler.running:
        return

    scheduler.add_job(
        func=lambda: app.app_context().push() or check_interview_reminders(),
        trigger="interval",
        minutes=1
    )

    scheduler.start()

    print("Interview Reminder Scheduler Started")