import os

from flask import url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

from app import mail


from flask import current_app

def get_serializer():
    secret_key = None
    try:
        if current_app:
            secret_key = current_app.config.get("SECRET_KEY")
    except Exception:
        pass
    if not secret_key:
        secret_key = os.getenv("SECRET_KEY", "default-fallback-secret-key-12345")
    return URLSafeTimedSerializer(secret_key)


def generate_verification_token(email):
    serializer = get_serializer()
    return serializer.dumps(
        email,
        salt="email-verification"
    )


def verify_verification_token(token, expiration=3600):
    serializer = get_serializer()
    try:
        email = serializer.loads(
            token,
            salt="email-verification",
            max_age=expiration
        )
        return email
    except Exception:
        return None



def send_verification_email(user):
    try:
        token = generate_verification_token(user.email)

        try:
            from flask import request
            base_url = request.host_url.rstrip('/')
            verification_url = f"{base_url}{url_for('auth.verify_email', token=token)}"
        except Exception:
            verification_url = url_for(
                "auth.verify_email",
                token=token,
                _external=True
            )

        msg = Message(
            subject="Verify Your JobTracker AI Account",
            sender=os.getenv("MAIL_USERNAME") or os.getenv("MAIL_DEFAULT_SENDER"),
            recipients=[user.email]
        )

        msg.body = f"""
Hello {user.name},

Welcome to JobTracker AI!

Thank you for registering.

Please verify your email by clicking the link below:

{verification_url}

This verification link expires in 1 hour.

If you did not create this account, you can safely ignore this email.

Regards,
JobTracker AI
"""

        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending verification email: {e}")
        return False



def generate_reset_token(email):
    serializer = get_serializer()
    return serializer.dumps(
        email,
        salt="password-reset"
    )


def verify_reset_token(token, expiration=3600):
    serializer = get_serializer()
    try:
        email = serializer.loads(
            token,
            salt="password-reset",
            max_age=expiration
        )
        return email
    except Exception:
        return None



def send_password_reset_email(user):
    try:
        token = generate_reset_token(user.email)
        try:
            from flask import request
            base_url = request.host_url.rstrip('/')
            reset_url = f"{base_url}{url_for('auth.reset_password', token=token)}"
        except Exception:
            reset_url = url_for(
                "auth.reset_password",
                token=token,
                _external=True
            )
        msg = Message(
            subject="Reset Your JobTracker AI Password",
            sender=os.getenv("MAIL_USERNAME") or os.getenv("MAIL_DEFAULT_SENDER"),
            recipients=[user.email]
        )
        msg.body = f"""
Hello {user.name},
We received a request to reset your password.
Click the link below to create a new password:
{reset_url}
This link expires in 1 hour.
If you didn't request this, simply ignore this email.
Regards,
JobTracker AI
"""
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending password reset email: {e}")
        return False


def send_test_email(receiver_email):
    try:
        msg = Message(
            subject="JobTracker AI - Test Email",
            sender=os.getenv("MAIL_USERNAME") or os.getenv("MAIL_DEFAULT_SENDER"),
            recipients=[receiver_email]
        )

        msg.body = """
Hello!

Congratulations 🎉

Your JobTracker AI email system is working successfully.

We'll use this system later for:

- Email Verification
- Interview Reminder Emails

Regards,
JobTracker AI
"""

        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending test email: {e}")
        return False


def send_interview_reminder(reminder):
    try:
        msg = Message(
            subject="Interview Reminder - JobTracker AI",
            sender=os.getenv("MAIL_USERNAME") or os.getenv("MAIL_DEFAULT_SENDER"),
            recipients=[reminder.user.email]
        )

        msg.body = f"""
Hello {reminder.user.name},

This is a reminder about your upcoming interview.

Company: {reminder.application.company}
Role: {reminder.application.role}

Interview Date:
{reminder.interview_date}

Interview Time:
{reminder.interview_time.strftime("%I:%M %p")}

Good luck!

Regards,
JobTracker AI
"""

        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending reminder email: {e}")
        return False