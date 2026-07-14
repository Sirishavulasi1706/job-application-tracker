import os

from flask import (
    Blueprint,
    render_template,
    current_app
)

from flask_login import login_required
from werkzeug.utils import secure_filename

from app.forms import JobMatchForm
from app.ai.resume_parser import extract_text_from_pdf
from app.ai.job_matcher import analyze_job_match

job_match = Blueprint("job_match", __name__)


@job_match.route("/job-match", methods=["GET", "POST"])
@login_required
def job_match_page():

    form = JobMatchForm()

    if form.validate_on_submit():

        file = form.resume.data

        filename = secure_filename(file.filename)

        upload_folder = current_app.config["UPLOAD_FOLDER"]

        os.makedirs(upload_folder, exist_ok=True)

        filepath = os.path.join(upload_folder, filename)

        file.save(filepath)

        resume_text = extract_text_from_pdf(filepath)

        result = analyze_job_match(
            resume_text,
            form.job_description.data
        )

        return render_template(
            "job_match.html",
            form=form,
            result=result
        )

    return render_template(
        "job_match.html",
        form=form
    )