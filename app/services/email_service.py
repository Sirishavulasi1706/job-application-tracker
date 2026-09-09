import os
import resend
from flask import url_for, current_app
from itsdangerous import URLSafeTimedSerializer

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
    return serializer.dumps(email, salt="email-verification")


def verify_verification_token(token, expiration=3600):
    serializer = get_serializer()
    try:
        return serializer.loads(token, salt="email-verification", max_age=expiration)
    except Exception:
        return None


def generate_reset_token(email):
    serializer = get_serializer()
    return serializer.dumps(email, salt="password-reset")


def verify_reset_token(token, expiration=3600):
    serializer = get_serializer()
    try:
        return serializer.loads(token, salt="password-reset", max_age=expiration)
    except Exception:
        return None


def send_mail_message(subject, recipient, body_text):
    """
    Sends an email using Resend over HTTPS (Render-friendly).
    Falls back to Flask-Mail if Resend is not configured.
    """
    resend_key = os.getenv("RESEND_API_KEY")
    if resend_key:
        try:
            resend.api_key = resend_key
            # Resend free sandbox requires sending from onboarding@resend.dev
            sender = "JobTracker AI <onboarding@resend.dev>"
            params = {
                "from": sender,
                "to": [recipient.strip()],
                "subject": subject,
                "text": body_text,
            }
            print(f"--> Sending email via Resend to {recipient}...", flush=True)
            res = resend.Emails.send(params)
            print(f"--> Resend response: {res}", flush=True)
            return True
        except Exception as e:
            print(f"--> Error sending email with Resend: {e}", flush=True)
            return False

    # Fallback to Flask-Mail SMTP if credentials exist
    mail_user = os.getenv("MAIL_USERNAME")
    mail_pass = os.getenv("MAIL_PASSWORD")
    if mail_user and mail_pass:
        try:
            from app import mail
            from flask_mail import Message
            msg = Message(
                subject=subject,
                sender=os.getenv("MAIL_DEFAULT_SENDER") or mail_user,
                recipients=[recipient]
            )
            msg.body = body_text
            mail.send(msg)
            return True
        except Exception as e:
            print(f"Error sending email with Flask-Mail: {e}")
            return False

    return False


def send_verification_email(user):
    try:
        token = generate_verification_token(user.email)
        try:
            from flask import request
            base_url = request.host_url.rstrip('/')
            verification_url = f"{base_url}{url_for('auth.verify_email', token=token)}"
        except Exception:
            verification_url = url_for("auth.verify_email", token=token, _external=True)

        body = f"""Hello {user.name},

Welcome to JobTracker AI! Thank you for registering.

Please verify your email by clicking the link below:
{verification_url}

This link expires in 1 hour.

Regards,
JobTracker AI
"""
        return send_mail_message("Verify Your JobTracker AI Account", user.email, body)
    except Exception as e:
        print(f"Error in send_verification_email: {e}")
        return False


def send_password_reset_email(user):
    try:
        token = generate_reset_token(user.email)
        try:
            from flask import request
            base_url = request.host_url.rstrip('/')
            reset_url = f"{base_url}{url_for('auth.reset_password', token=token)}"
        except Exception:
            reset_url = url_for("auth.reset_password", token=token, _external=True)

        body = f"""Hello {user.name},

We received a request to reset your password. Click the link below to set a new password:
{reset_url}

This link expires in 1 hour. If you did not request this, you can ignore this email.

Regards,
JobTracker AI
"""
        return send_mail_message("Reset Your JobTracker AI Password", user.email, body)
    except Exception as e:
        print(f"Error in send_password_reset_email: {e}")
        return False


def send_test_email(receiver_email):
    body = """Hello!

Congratulations 🎉
Your JobTracker AI email system is working successfully via Resend!

Regards,
JobTracker AI
"""
    return send_mail_message("JobTracker AI - Test Email", receiver_email, body)


def send_interview_reminder(reminder):
    try:
        body = f"""Hello {reminder.user.name},

This is a reminder about your upcoming interview.

Company: {reminder.application.company}
Role: {reminder.application.role}
Date: {reminder.interview_date}
Time: {reminder.interview_time.strftime("%I:%M %p")}

Good luck!

Regards,
JobTracker AI
"""
        return send_mail_message("Interview Reminder - JobTracker AI", reminder.user.email, body)
    except Exception as e:
        print(f"Error in send_interview_reminder: {e}")
        return False