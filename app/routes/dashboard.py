from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models import JobApplication, ResumeAnalysis
from app.ai.career_insights import generate_career_insights

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def dashboard_home():

    total_applications = JobApplication.query.filter_by(
        user_id=current_user.id
    ).count()

    total_resume_analyses = ResumeAnalysis.query.filter_by(
        user_id=current_user.id
    ).count()

    pending = JobApplication.query.filter_by(
        user_id=current_user.id,
        status="Applied"
    ).count()

    interviews = JobApplication.query.filter_by(
        user_id=current_user.id,
        status="Interview"
    ).count()

    offers = JobApplication.query.filter_by(
        user_id=current_user.id,
        status="Offered"
    ).count()

    rejected = JobApplication.query.filter_by(
        user_id=current_user.id,
        status="Rejected"
    ).count()

    recent_applications = (
        JobApplication.query
        .filter_by(user_id=current_user.id)
        .order_by(JobApplication.created_at.desc())
        .limit(5)
        .all()
    )

    # Get latest resume analysis
    latest_resume = (
        ResumeAnalysis.query
        .filter_by(user_id=current_user.id)
        .order_by(ResumeAnalysis.created_at.desc())
        .first()
    )

    career_insights = None

    if latest_resume:
        career_insights = generate_career_insights(
            latest_resume.analysis
        )

    return render_template(
        "dashboard.html",
        total_applications=total_applications,
        total_resume_analyses=total_resume_analyses,
        pending=pending,
        interviews=interviews,
        offers=offers,
        rejected=rejected,
        recent_applications=recent_applications,
        career_insights=career_insights
    )