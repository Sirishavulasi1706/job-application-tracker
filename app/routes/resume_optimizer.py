from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app import db
from app.models import (
    ResumeAnalysis,
    ResumeOptimization
)
from app.ai.resume_optimizer import optimize_resume


resume_optimizer = Blueprint(
    "resume_optimizer",
    __name__
)


@resume_optimizer.route(
    "/resume-optimizer",
    methods=["GET", "POST"]
)
@login_required
def optimizer():

    analyses = (
        ResumeAnalysis.query
        .filter_by(user_id=current_user.id)
        .order_by(
            ResumeAnalysis.created_at.desc()
        )
        .all()
    )

    optimization = None
    selected_analysis = None

    if request.method == "POST":

        analysis_id = request.form.get("analysis_id")
        job_description = request.form.get("job_description")

        selected_analysis = ResumeAnalysis.query.filter_by(
            id=analysis_id,
            user_id=current_user.id
        ).first()

        if selected_analysis:

            existing = ResumeOptimization.query.filter_by(
                resume_analysis_id=selected_analysis.id,
                job_description=job_description
            ).first()

            if existing:

                optimization = existing.optimization

            else:

                optimization = optimize_resume(
                    selected_analysis.analysis,
                    job_description
                )

                new_result = ResumeOptimization(
                    user_id=current_user.id,
                    resume_analysis_id=selected_analysis.id,
                    job_description=job_description,
                    optimization=optimization
                )

                db.session.add(new_result)
                db.session.commit()

    history = (
        ResumeOptimization.query
        .filter_by(
            user_id=current_user.id
        )
        .order_by(
            ResumeOptimization.created_at.desc()
        )
        .all()
    )

    history_data = []

    for item in history:

        resume_analysis = ResumeAnalysis.query.filter_by(
            id=item.resume_analysis_id,
            user_id=current_user.id
        ).first()

        history_data.append({
            "optimization": item.optimization,
            "job_description": item.job_description,
            "created_at": item.created_at,
            "resume_filename": (
                resume_analysis.resume_filename
                if resume_analysis
                else "Resume not found"
            )
        })

    return render_template(
        "resume_optimizer.html",
        analyses=analyses,
        optimization=optimization,
        selected_analysis=selected_analysis,
        history=history_data
    )