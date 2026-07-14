from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import or_

from app import db
from app.forms import ApplicationForm
from app.models import JobApplication

applications = Blueprint("applications", __name__)


@applications.route("/applications")
@login_required
def view_applications():

    search = request.args.get("search", "")
    status = request.args.get("status", "")

    query = JobApplication.query.filter_by(
        user_id=current_user.id
    )

    if search:
        query = query.filter(
            or_(
                JobApplication.company.ilike(f"%{search}%"),
                JobApplication.role.ilike(f"%{search}%")
            )
        )

    if status:
        query = query.filter(
            JobApplication.status == status
        )

    applications_list = query.order_by(
        JobApplication.created_at.desc()
    ).all()

    return render_template(
        "applications.html",
        applications=applications_list,
        search=search,
        status=status
    )


@applications.route("/add_application", methods=["GET", "POST"])
@login_required
def add_application():

    form = ApplicationForm()

    if form.validate_on_submit():

        application = JobApplication(
            company=form.company.data,
            role=form.role.data,
            location=form.location.data,
            status=form.status.data,
            job_link=form.job_link.data,
            applied_date=form.applied_date.data,
            notes=form.notes.data,
            user_id=current_user.id
        )

        db.session.add(application)
        db.session.commit()

        flash("Job application added successfully!", "success")

        return redirect(url_for("applications.view_applications"))

    return render_template("add_application.html", form=form)


@applications.route("/edit_application/<int:id>", methods=["GET", "POST"])
@login_required
def edit_application(id):

    application = JobApplication.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    form = ApplicationForm(obj=application)

    if form.validate_on_submit():

        application.company = form.company.data
        application.role = form.role.data
        application.location = form.location.data
        application.status = form.status.data
        application.job_link = form.job_link.data
        application.applied_date = form.applied_date.data
        application.notes = form.notes.data

        db.session.commit()

        flash("Application updated successfully!", "success")

        return redirect(url_for("applications.view_applications"))

    return render_template("add_application.html", form=form)


@applications.route("/delete_application/<int:id>")
@login_required
def delete_application(id):

    application = JobApplication.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(application)
    db.session.commit()

    flash("Application deleted successfully!", "success")

    return redirect(url_for("applications.view_applications"))