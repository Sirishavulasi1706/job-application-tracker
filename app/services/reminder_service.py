
from datetime import datetime, timedelta

from flask_mail import Message

from app import db, mail
from app.models import InterviewReminder


def send_interview_reminder(reminder):

    application = reminder.application
    user = application.user

    msg = Message(
        subject="Interview Reminder - JobTracker AI",
        recipients=[user.email]
    )

    msg.body = f"""
Hello {user.name},

This is a reminder about your upcoming interview.

Company: {application.company}
Role: {application.role}

Date: {reminder.interview_date}
Time: {reminder.interview_time}

Good luck!

Regards,
JobTracker AI
"""

    mail.send(msg)

    reminder.reminder_sent = True

    db.session.commit()

