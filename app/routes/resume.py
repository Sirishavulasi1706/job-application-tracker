import os

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    current_app
)

from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.ai.resume_parser import extract_text_from_pdf
from app.ai.gemini_service import analyze_resume
from app.models import ResumeAnalysis
from app import db

resume = Blueprint("resume", __name__)


@resume.route("/resume", methods=["GET", "POST"])
@login_required
def upload_resume():

    if request.method == "POST":

        if "resume" not in request.files:
            flash("No file selected.", "danger")
            return render_template("resume.html")

        file = request.files["resume"]

        if file.filename == "":
            flash("Please choose a PDF.", "danger")
            return render_template("resume.html")

        upload_folder = current_app.config["UPLOAD_FOLDER"]

        os.makedirs(upload_folder, exist_ok=True)

        filename = secure_filename(file.filename)

        filepath = os.path.join(upload_folder, filename)

        file.save(filepath)

        resume_text = extract_text_from_pdf(filepath)

        analysis = analyze_resume(resume_text)

        new_analysis = ResumeAnalysis(
            user_id=current_user.id,
            resume_filename=filename,
            analysis=analysis
        )

        db.session.add(new_analysis)
        db.session.commit()

        return render_template(
            "resume.html",
            analysis=analysis
        )

    return render_template("resume.html")