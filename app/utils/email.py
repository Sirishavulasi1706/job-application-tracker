
import os

from flask import url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

from app import mail


def generate_verification_token(email):

    serializer = URLSafeTimedSerializer(
        os.getenv("SECRET_KEY")
    )

    return serializer.dumps(
        email,
        salt="email-verification"
    )


def verify_verification_token(token, expiration=3600):

    serializer = URLSafeTimedSerializer(
        os.getenv("SECRET_KEY")
    )

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

    token = generate_verification_token(user.email)

    verification_url = url_for(
        "auth.verify_email",
        token=token,
        _external=True
    )

    msg = Message(
        subject="Verify Your JobTracker AI Account",
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


def send_test_email(receiver_email):

    msg = Message(
        subject="JobTracker AI - Test Email",
        recipients=[receiver_email]
    )

    msg.body = """
Hello!

Congratulations 🎉

Your JobTracker AI email system is working successfully.

We'll use this system later for:

• Email Verification
• Interview Reminder Emails

Regards,
JobTracker AI
"""

    mail.send(msg)

