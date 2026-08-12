from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    send_file
)
from flask_login import login_required, current_user

from app import db
from app.models import ResumeBuilder
from app.services.resume_builder_service import generate_resume
from app.services.pdf_service import create_cover_letter_pdf

resume_builder = Blueprint("resume_builder", __name__)


@resume_builder.route("/resume-builder", methods=["GET", "POST"])
@login_required
def builder():

    generated_resume = None

    if request.method == "POST":

        generated_resume = generate_resume(
            request.form["full_name"],
            request.form["email"],
            request.form["phone"],
            request.form["linkedin"],
            request.form["github"],
            request.form["portfolio"],
            request.form["education"],
            request.form["skills"],
            request.form["experience"],
            request.form["projects"],
            request.form["certifications"],
            request.form["achievements"],
        )

        resume = ResumeBuilder(
            user_id=current_user.id,
            full_name=request.form["full_name"],
            email=request.form["email"],
            phone=request.form["phone"],
            linkedin=request.form["linkedin"],
            github=request.form["github"],
            portfolio=request.form["portfolio"],
            education=request.form["education"],
            skills=request.form["skills"],
            experience=request.form["experience"],
            projects=request.form["projects"],
            certifications=request.form["certifications"],
            achievements=request.form["achievements"],
            generated_resume=generated_resume,
        )

        db.session.add(resume)
        db.session.commit()

        flash("Resume generated successfully!", "success")

    return render_template(
        "resume_builder.html",
        generated_resume=generated_resume,
    )


@resume_builder.route("/resume-history")
@login_required
def history():

    resumes = (
        ResumeBuilder.query
        .filter_by(user_id=current_user.id)
        .order_by(ResumeBuilder.created_at.desc())
        .all()
    )

    return render_template(
        "resume_history.html",
        resumes=resumes
    )


@resume_builder.route("/resume/<int:id>")
@login_required
def view_resume(id):

    resume = ResumeBuilder.query.get_or_404(id)

    return render_template(
        "resume_view.html",
        resume=resume
    )


@resume_builder.route("/resume/delete/<int:id>")
@login_required
def delete_resume(id):

    resume = ResumeBuilder.query.get_or_404(id)

    db.session.delete(resume)
    db.session.commit()

    flash("Resume deleted successfully!", "success")

    return redirect(url_for("resume_builder.history"))


@resume_builder.route(
    "/resume/download/<int:id>"
)
@login_required
def download_resume(id):

    resume = ResumeBuilder.query.get_or_404(id)

    pdf = create_cover_letter_pdf(
        resume.generated_resume
    )

    return send_file(
        pdf,
        as_attachment=True,
        download_name="resume.pdf",
        mimetype="application/pdf",
    )