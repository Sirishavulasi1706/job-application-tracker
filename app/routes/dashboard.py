
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models import JobApplication, ResumeAnalysis

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def dashboard_home():

    applications = JobApplication.query.filter_by(
        user_id=current_user.id
    ).all()

    total_applications = len(applications)

    total_resume_analyses = ResumeAnalysis.query.filter_by(
        user_id=current_user.id
    ).count()

    pending = sum(a.status == "Applied" for a in applications)

    interviews = sum(a.status == "Interview" for a in applications)

    offers = sum(a.status == "Offered" for a in applications)

    rejected = sum(a.status == "Rejected" for a in applications)

    success_rate = 0

    if total_applications:

        success_rate = round(
            (offers / total_applications) * 100
        )

    interview_rate = 0

    if total_applications:

        interview_rate = round(
            (interviews / total_applications) * 100
        )

    recent_applications = sorted(
        applications,
        key=lambda x: x.created_at,
        reverse=True
    )[:5]

    latest_resume = (
        ResumeAnalysis.query
        .filter_by(user_id=current_user.id)
        .order_by(ResumeAnalysis.created_at.desc())
        .first()
    )

    career_insights = None

    if latest_resume:
        career_insights = latest_resume.career_insights

    return render_template(
        "dashboard.html",

        total_applications=total_applications,

        total_resume_analyses=total_resume_analyses,

        pending=pending,

        interviews=interviews,

        offers=offers,

        rejected=rejected,

        success_rate=success_rate,

        interview_rate=interview_rate,

        recent_applications=recent_applications,

        career_insights=career_insights
    )

