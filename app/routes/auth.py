import os
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.forms import (
    RegistrationForm,
    LoginForm,
    ForgotPasswordForm,
    ResetPasswordForm
)
from app.models import User
from app import db, bcrypt
from app.services.email_service import (
    send_verification_email,
    verify_verification_token,
    send_password_reset_email
)

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(
            email=form.email.data
        ).first()

        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")

        mail_user = os.getenv("MAIL_USERNAME")
        mail_pass = os.getenv("MAIL_PASSWORD")
        has_mail = bool(mail_user and mail_pass)

        if existing_user:
            if existing_user.email_verified:
                flash("Email already registered. Please log in.", "info")
                return redirect(url_for("auth.login"))
            else:
                # Update unverified user with new credentials
                existing_user.name = form.name.data
                existing_user.password = hashed_password
                if not has_mail:
                    existing_user.email_verified = True
                    db.session.commit()
                    flash("Account verified successfully! You can now log in.", "success")
                    return redirect(url_for("auth.login"))
                else:
                    db.session.commit()
                    sent = send_verification_email(existing_user)
                    if sent:
                        flash("A verification link has been sent to your email.", "info")
                    else:
                        existing_user.email_verified = True
                        db.session.commit()
                        flash("Account registered successfully! You can now log in.", "success")
                    return redirect(url_for("auth.login"))

        # Create new user
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
            email_verified=not has_mail
        )
        db.session.add(user)
        db.session.commit()

        if has_mail:
            sent = send_verification_email(user)
            if sent:
                flash(
                    "Registration successful! Please check your email to verify your account.",
                    "success"
                )
            else:
                # Fallback: if email fails to send, auto-verify user so they are not blocked
                user.email_verified = True
                db.session.commit()
                flash(
                    "Registration successful! You can now log in.",
                    "success"
                )
        else:
            flash(
                "Registration successful! You can now log in.",
                "success"
            )

        return redirect(url_for("auth.login"))

    return render_template(
        "register.html",
        form=form
    )

@auth.route("/verify/<token>")
def verify_email(token):
    email = verify_verification_token(token)
    if not email:
        flash(
            "Verification link is invalid or has expired.",
            "danger"
        )
        return redirect(url_for("auth.login"))
    user = User.query.filter_by(email=email).first()
    if not user:
        flash(
            "User not found.",
            "danger"
        )
        return redirect(url_for("auth.login"))
    if user.email_verified:
        flash(
            "Email is already verified.",
            "info"
        )
        return redirect(url_for("auth.login"))
    user.email_verified = True
    db.session.commit()
    flash(
        "Email verified successfully! You can now log in.",
        "success"
    )
    return redirect(url_for("auth.login"))

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data
        ).first()
        if user and bcrypt.check_password_hash(
            user.password,
            form.password.data
        ):
            mail_user = os.getenv("MAIL_USERNAME")
            mail_pass = os.getenv("MAIL_PASSWORD")
            has_mail = bool(mail_user and mail_pass)

            if not user.email_verified and not has_mail:
                user.email_verified = True
                db.session.commit()

            if not user.email_verified:
                flash(
                    "Please verify your email before logging in.",
                    "warning"
                )
                return redirect(url_for("auth.login"))
            login_user(user)
            flash(
                "Login successful!",
                "success"
            )
            return redirect(
                url_for("dashboard.dashboard_home")
            )
        flash(
            "Invalid email or password.",
            "danger"
        )
    return render_template(
        "login.html",
        form=form
    )

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash(
        "Logged out successfully.",
        "success"
    )
    return redirect(url_for("main.home"))
@auth.route("/resend-verification/<email>")
def resend_verification(email):
    user = User.query.filter_by(email=email).first()
    if user and not user.email_verified:
        sent = send_verification_email(user)
        if sent:
            flash(
                "Verification email sent successfully.",
                "success"
            )
        else:
            user.email_verified = True
            db.session.commit()
            flash(
                "Account auto-verified! You can now log in.",
                "success"
            )
    else:
        flash(
            "Account already verified.",
            "info"
        )
    return redirect(url_for("auth.login"))


@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    form = ForgotPasswordForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user:

            send_password_reset_email(user)

        flash(
            "If an account exists with that email, a password reset link has been sent.",
            "info"
        )

        return redirect(url_for("auth.login"))

    return render_template(
        "forgot_password.html",
        form=form
    )


@auth.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):

    email = User.verify_reset_token(token)

    if not email:

        flash(
            "The password reset link is invalid or has expired.",
            "danger"
        )

        return redirect(url_for("auth.forgot_password"))

    user = User.query.filter_by(email=email).first()

    form = ResetPasswordForm()

    if form.validate_on_submit():

        user.password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")

        db.session.commit()

        flash(
            "Your password has been reset successfully. Please log in.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template(
        "reset_password.html",
        form=form
    )