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


def extract_career_insights(analysis):

    if not analysis:
        return None

    marker = "CAREER INSIGHTS:"

    if marker not in analysis:
        return None

    insights = analysis.split(marker, 1)[1]

    next_sections = [
        "RECOMMENDATIONS:",
        "RESUME SCORE:",
        "STRENGTHS:",
        "WEAKNESSES:",
        "SKILLS ANALYSIS:",
        "PROJECT ANALYSIS:",
        "EXPERIENCE ANALYSIS:",
        "ATS ANALYSIS:"
    ]

    for section in next_sections:

        if section in insights:
            insights = insights.split(section, 1)[0]

    insights = insights.strip()

    if insights:
        return insights

    return None


@resume.route("/resume", methods=["GET", "POST"])
@login_required
def upload_resume():

    if request.method == "POST":

        if "resume" not in request.files:

            flash(
                "No file selected.",
                "danger"
            )

            return render_template("resume.html")

        file = request.files["resume"]

        if file.filename == "":

            flash(
                "Please choose a PDF.",
                "danger"
            )

            return render_template("resume.html")

        upload_folder = current_app.config["UPLOAD_FOLDER"]

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        filename = secure_filename(
            file.filename
        )

        filepath = os.path.join(
            upload_folder,
            filename
        )

        file.save(filepath)

        resume_text = extract_text_from_pdf(
            filepath
        )

        if not resume_text:

            flash(
                "Could not extract text from the resume.",
                "danger"
            )

            return render_template("resume.html")

        analysis = analyze_resume(
            resume_text
        )

        career_insights = extract_career_insights(
            analysis
        )

        new_analysis = ResumeAnalysis(
            user_id=current_user.id,
            resume_filename=filename,
            analysis=analysis,
            career_insights=career_insights
        )

        db.session.add(
            new_analysis
        )

        db.session.commit()

        flash(
            "Resume analyzed successfully!",
            "success"
        )

        return render_template(
            "resume.html",
            analysis=analysis
        )

    return render_template(
        "resume.html"
    )