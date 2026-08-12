from flask import Blueprint, render_template, request, flash, send_file
from flask_login import login_required, current_user

from app import db
from app.models import CoverLetter
from app.services.cover_letter_service import generate_cover_letter
from app.services.pdf_service import create_cover_letter_pdf


cover_letter = Blueprint(
    "cover_letter",
    __name__
)


@cover_letter.route(
    "/cover-letter",
    methods=["GET", "POST"]
)
@login_required
def cover_letter_generator():

    generated_letter = None

    if request.method == "POST":

        company = request.form.get("company")

        role = request.form.get("role")

        job_description = request.form.get("job_description")

        try:

            generated_letter = generate_cover_letter(
                company,
                role,
                job_description
            )

            letter = CoverLetter(

                user_id=current_user.id,

                company=company,

                role=role,

                job_description=job_description,

                cover_letter=generated_letter

            )

            db.session.add(letter)

            db.session.commit()

            flash(
                "Cover letter generated successfully!",
                "success"
            )

        except Exception as e:

            flash(
                f"Error: {e}",
                "danger"
            )

    return render_template(
        "cover_letter.html",
        generated_letter=generated_letter
    )


@cover_letter.route("/download-cover-letter", methods=["POST"])
@login_required
def download_cover_letter():

    cover_letter = request.form.get("cover_letter")

    pdf = create_cover_letter_pdf(cover_letter)

    return send_file(
        pdf,
        as_attachment=True,
        download_name="cover_letter.pdf",
        mimetype="application/pdf"
    )