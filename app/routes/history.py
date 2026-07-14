from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models import ResumeAnalysis

history = Blueprint("history", __name__)


@history.route("/history")
@login_required
def history_page():

    analyses = ResumeAnalysis.query.filter_by(
        user_id=current_user.id
    ).order_by(
        ResumeAnalysis.created_at.desc()
    ).all()

    return render_template(
        "history.html",
        analyses=analyses
    )